import os
import time
from pdf_oxide import PdfDocument, Pdf, split_by_bookmarks, plan_split_by_bookmarks

LOCAL_PDF_PATH = r"D:\1111.pdf"


def split_to_pages_oxide(pdf_path):
    """使用 pdf_oxide 将 PDF 拆分为单页，返回每页 bytes 列表"""
    doc = PdfDocument(pdf_path)
    n = doc.page_count()
    ranges = [(i, i + 1) for i in range(n)]
    pages = doc.extract_page_ranges_to_bytes(ranges)
    return pages


def split_by_bookmarks_oxide(pdf_path):
    """使用 pdf_oxide 按书签拆分 PDF"""
    with open(pdf_path, "rb") as f:
        src_bytes = f.read()

    try:
        segments = split_by_bookmarks(src_bytes)
    except RuntimeError:
        return []  # 没有书签

    results = []
    for meta, seg_bytes in segments:
        results.append({
            "title": meta.get("title", ""),
            "start_page": meta.get("start_page"),
            "end_page": meta.get("end_page"),
            "file_stem": meta.get("file_stem", ""),
            "bytes": seg_bytes,
        })
    return results


def main():
    print(f"PDF 文件: {LOCAL_PDF_PATH}")
    print(f"文件大小: {os.path.getsize(LOCAL_PDF_PATH) / 1024:.1f} KB\n")

    # --- 拆分为单页 ---
    start = time.perf_counter()
    pages = split_to_pages_oxide(LOCAL_PDF_PATH)
    elapsed = time.perf_counter() - start
    print(f"[单页拆分] -> {len(pages)} 页, 耗时: {elapsed:.4f}s")

    # --- 按书签拆分 ---
    print(f"\n[书签拆分]")
    with open(LOCAL_PDF_PATH, "rb") as f:
        try:
            plan = plan_split_by_bookmarks(f.read())
        except RuntimeError:
            plan = []

    if plan:
        for item in plan:
            print(f"  {item['file_stem']}: 第 {item['start_page']}-{item['end_page']} 页 → {item['title']}")

        start = time.perf_counter()
        segments = split_by_bookmarks_oxide(LOCAL_PDF_PATH)
        elapsed = time.perf_counter() - start
        print(f"  生成 {len(segments)} 个分段, 耗时: {elapsed:.4f}s")
    else:
        print(f"  该 PDF 没有书签(outline)，跳过")

    # --- 合并回单页 ---
    print(f"\n[合并验证]")
    tmp_dir = os.path.join(os.path.dirname(LOCAL_PDF_PATH), "_oxide_tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    page_paths = []
    for i, page_data in enumerate(pages):
        p = os.path.join(tmp_dir, f"page_{i + 1}.pdf")
        with open(p, "wb") as f:
            f.write(page_data)
        page_paths.append(p)

    try:
        start = time.perf_counter()
        merged = Pdf.merge(page_paths)
        merged.save(os.path.join(tmp_dir, "merged.pdf"))
        elapsed = time.perf_counter() - start
        print(f"  {len(page_paths)} 页合并 -> merged.pdf, 耗时: {elapsed:.4f}s")
    finally:
        for p in page_paths:
            if os.path.exists(p):
                os.remove(p)
        merged_pdf = os.path.join(tmp_dir, "merged.pdf")
        if os.path.exists(merged_pdf):
            os.remove(merged_pdf)
        os.rmdir(tmp_dir)


if __name__ == "__main__":
    main()
