#!/usr/bin/env python3
"""
generate_marketing_meta.py - High-CTR Curiosity Titles, Debate Comments, Descriptions & Affiliate Packages
Specialized for TikTok, YouTube Shorts & Facebook Reels for 56+ Book Summary Videos.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIGS_DIR = BASE_DIR / "configs"

# Default Shopee Affiliate template (user can replace affiliate tag)
DEFAULT_AFF_BASE = "https://s.shopee.vn/affiliate_book"

# Handcrafted High-Converting Curiosity Metadata for Key Book Archetypes
CURATED_MARKETING_PACK = {
    "xa_hoi_met_moi": {
        "title_curiosity": "Càng Cố Gắng 'Chữa Lành', Bạn Càng Bế Tắc?",
        "alternative_titles": [
            "Tại Sao Bạn Luôn Cảm Thấy Mình Là Kẻ Bất Tài Lúc 2h Sáng?",
            "Sự Thật Đằng Sau Trào Lưu 'Chữa Lành' Của Giới Trẻ",
            "Tự Bóc Lột Bản Thân: Căn Bệnh Nguy Hiểm Nhất Thời Đại",
            "Đừng Tự Hào Vì Bạn Đang Quá Bận Rộn!"
        ],
        "debate_question": "Bạn có đồng ý rằng: 'Chữa lành' thực chất là cái cớ để trốn tránh sự yếu kém của bản thân? Bạn đang làm việc vì đam mê hay đang tự biến mình thành nô lệ?",
        "callout": "Nếu bạn thấy đầu óc luôn căng cứng và cảm giác như một chú chuột chạy vô tận trên bánh xe, cuốn sách này sinh ra là để tát nước lạnh vào bạn."
    },
    "dac_nhan_tam": {
        "title_curiosity": "Đừng Đọc Đắc Nhân Tâm Nếu Bạn Sợ Giả Tạo!",
        "alternative_titles": [
            "Mặt Tối Của Đắc Nhân Tâm Mà Không Ai Dám Nói",
            "Sống Quá Tử Tế Ở Xã Hội Này Thực Chất Là Một Sự HÈN NHÁT?",
            "Lý Do Càng Cố Làm Hài Lòng Mọi Người, Bạn Càng Bị Coi Thường",
            "Nghệ Thuật Thu Phục Lòng Người Hay Kỹ Năng Thao Túng Tinh Vi?"
        ],
        "debate_question": "Sống tử tế và sống giả tạo để được lòng người khác khác nhau ở chỗ nào? Bạn đã từng bị 'phản bội' chỉ vì quá tốt với người khác chưa?",
        "callout": "Cuốn sách bị hiểu lầm nhiều nhất mọi thời đại. Nó không dạy bạn luồn cúi, nó dạy bạn cách sống sót giữa lòng người hiểm độc."
    },
    "dam_bi_ghet": {
        "title_curiosity": "Chừng Nào Còn Sợ Bị Ghét, Bạn Còn Làm Nô Lệ!",
        "alternative_titles": [
            "Bí Mật Để Không Bao Giờ Bị Thao Túng Tâm Lý",
            "Tại Sao Người Dám Bị Ghét Lại Sống Hạnh Phúc Nhất?",
            "Đừng Cố Hòa Nhập Khi Bạn Sinh Ra Không Phải Để Làm Hài Lòng Kẻ Khác",
            "Sự Thật Phũ Phàng: 99% Mọi Người Chẳng Quan Tâm Đến Bạn Đâu!"
        ],
        "debate_question": "Giữa 'Được mọi người quý mến nhưng sống giả tạo' và 'Bị nhiều người ghét nhưng được sống thật với chính mình', bạn chọn cái nào?",
        "callout": "Một cuốn sách triết học Adler kinh điển sẽ bẻ gãy mọi sợi dây xích vô hình đang trói buộc bạn vào định kiến của gia đình và xã hội."
    },
    "tam_ly_hoc_ve_tien": {
        "title_curiosity": "Lý Do Người Chăm Chỉ Vẫn Nghèo Cả Đời!",
        "alternative_titles": [
            "Sự Thật Tàn Nhẫn Về Tiền Bạc Người Nghèo Không Bao Giờ Biết",
            "Tại Sao Kiếm Được Nhiều Tiền Vẫn Rơi Vào Bẫy Rỗng Túi?",
            "Nghịch Lý Giàu Có: Người Càng Khoe Khoang Càng Bất An",
            "Quy Luật Tiền Bạc Đơn Giản Nhất Nhưng 90% Mọi Người Làm Ngược Lại"
        ],
        "debate_question": "Theo bạn: Giàu có là do may mắn, năng lực hay do kỷ luật thép quản lý cảm xúc? Điều ngu ngốc nhất bạn từng làm với tiền là gì?",
        "callout": "Cách bạn đối xử với tiền quan trọng gấp 10 lần việc bạn kiếm được bao nhiêu tiền. Đây là cuốn sách gối đầu giường về tâm lý tài chính."
    }
    ,
    "atomic_habits": {
        "title_curiosity": "Bí Mật 1% Khiến Kẻ Lười Biếng Thành Xuất Chúng!",
        "alternative_titles": [
            "Đừng Đặt Mục Tiêu Nữa, Hãy Làm Việc Này Thay Thế!",
            "Lý Do Bạn Bỏ Cuộc Sau 3 Ngày Bắt Đầu Kỷ Luật",
            "Cách Não Bộ Lừa Bạn Trì Hoãn Suốt Nhiều Năm",
            "Chiến Lược Thay Đổi Bản Thân Mà Không Cần Ý Chí Thần Thánh"
        ],
        "debate_question": "Bạn đã bao giờ quyết tâm dậy sớm tập thể dục rồi bỏ cuộc chỉ sau 3 ngày chưa? Theo bạn, rào cản lớn nhất của kỷ luật là gì?",
        "callout": "Cuốn sách thực tế nhất về thói quen nguyên tử. Không hô hào khẩu hiệu, chỉ có phương pháp khoa học từng bước nhỏ."
    },
    "cant_hurt_me": {
        "title_curiosity": "Bạn Không Kiệt Sức, Bạn Chỉ Đang Tự Nuông Chiều!",
        "alternative_titles": [
            "Quy Tắc 40%: Bí Mật Của Kẻ Bất Khả Chiến Bại",
            "Lời Tự Thú Của Người Đàn Ông Dai Sức Nhất Hành Tinh",
            "Tại Sao Nỗi Đau Là Thứ Duy Nhất Cứu Được Bạn?",
            "Dừng Than Vãn Và Bắt Đầu Chịu Trách Nhiệm Về Cuộc Đời Mình!"
        ],
        "debate_question": "Khi muốn bỏ cuộc, bạn thường tự nhủ điều gì? Bạn tin vào 'chữa lành bằng sự dịu dàng' hay 'tôi luyện qua gian khổ'?",
        "callout": "David Goggins sẽ đập tan mọi lý do thoái thác và lười biếng sâu thẳm trong bạn. Đọc để biết giới hạn thật sự của mình ở đâu."
    },
    "48_quy_tac_quyen_luc": {
        "title_curiosity": "Tại Sao Kẻ Xảo Quyệt Thường Thắng Người Lương Thiện?",
        "alternative_titles": [
            "Quy Tắc Ngầm Nơi Công Sở Bạn Không Bao Giờ Được Dạy",
            "Đừng Bao Giờ Lấn Át Sếp Nếu Không Muốn Bị Trừ Khử",
            "Nghệ Thuật Ẩn Mình Và Thao Túng Cục Diện Trong Im Lặng",
            "Sự Thật Khắc Nghiệt Về Quyền Lực Bạn Phải Biết Trước Tuổi 30"
        ],
        "debate_question": "Nơi công sở hay ngoài xã hội, người có năng lực thật sự hay người giỏi lấy lòng cấp trên sẽ thăng tiến nhanh hơn?",
        "callout": "Cuốn sách cẩm nang quyền lực chân thực và gai góc nhất. Không đọc để hại người, mà để không bị kẻ khác dẫm đạp."
    },
    "deep_work": {
        "title_curiosity": "Não Bạn Đang Bị TikTok Và Shorts 'Hủy Hoại' Thế Nào?",
        "alternative_titles": [
            "Hội Chứng Sương Mù Não Và Cách Cứu Lấy Sự Tập Trung",
            "Kỹ Năng Đắt Giá Nhất Kỷ Nguyên AI Mà 95% Đã Đánh Mất",
            "Tại Sao Ngồi Vào Bàn 8 Tiếng Nhưng Chỉ Làm Việc Được 30 Phút?",
            "Làm Việc Sâu: Bí Mật Để Tăng Gấp 5 Lần Hiệu Suất"
        ],
        "debate_question": "Khoảng thời gian dài nhất bạn có thể tập trung làm một việc mà không sờ vào điện thoại là bao lâu? Thừa nhận thật lòng xem nào!",
        "callout": "Sự tập trung sâu là siêu năng lực của thế kỷ 21. Cuốn sách này sẽ hướng dẫn bạn cai nghiện dopamine và làm chủ lại não bộ."
    }

}
def build_dynamic_titles(title: str, author: str, core_msg: str) -> Tuple[str, List[str]]:
    """Generate high-curiosity titles based on psychological triggers if not in curated list."""
    clean_title = title.split("(")[0].strip()
    
    # 4 psychological hook formulas
    t1 = f"Tại Sao Càng Sống Tốt Bạn Càng Bị Coi Thường? | {clean_title}"
    if len(t1) > 65:
        t1 = f"Tại Sao Càng Sống Tốt Bạn Càng Bế Tắc?"

    templates = [
        f"Sự Thật Tàn Nhẫn Ít Ai Dám Nói Trong {clean_title}",
        f"Dừng Lại 60s Nếu Bạn Đang Thấy Bế Tắc Về Cuộc Đời",
        f"Lý Do Người Chăm Chỉ Vẫn Không Thể Thành Công",
        f"Bí Mật Tâm Lý Giúp Bạn Ngừng Sợ Hãi Định Kiến",
        f"Đừng Đọc {clean_title} Nếu Bạn Vẫn Muốn Sống Tự Lừa Dối!"
    ]
    
    # Custom tailored dynamic heuristics
    if any(k in core_msg.lower() for k in ["tiền", "tài chính", "nợ", "giàu"]):
        t1 = f"Lý Do Bạn Kiếm Bao Nhiêu Tiền Vẫn Rỗng Túi?"
        templates[0] = f"Bẫy Tài Chính Khiến 90% Người Trẻ Không Thể Giàu"
        templates[1] = f"Sự Thật Phũ Phàng Về Tiền Bạc Mà Trường Học Giấu Bạn"
    elif any(k in core_msg.lower() for k in ["lo âu", "stress", "mệt mỏi", "kiệt sức", "chữa lành"]):
        t1 = f"Bạn Đang Tổn Thương Thật Hay Chỉ Đang Trốn Tránh?"
        templates[0] = f"Tại Sao Càng Cố 'Chữa Lành' Bạn Càng Trầm Cảm?"
        templates[1] = f"Hội Chứng Tự Hành Hạ Bản Thân Lúc 2 Giờ Sáng"
    elif any(k in core_msg.lower() for k in ["kỷ luật", "thói quen", "trì hoãn", "lười"]):
        t1 = f"Động Lực Là Rác Rưởi, Kỷ Luật Mới Cứu Được Bạn!"
        templates[0] = f"Cách Đập Tan Trì Hoãn Trong Đúng 5 Giây"
        templates[1] = f"Bí Mật Để Não Bộ Tự Động Kỷ Luật Không Cần Gồng Mình"
    elif any(k in core_msg.lower() for k in ["thao túng", "tâm lý", "lừa dối", "đám đông"]):
        t1 = f"3 Dấu Hiệu Bạn Đang Bị Thao Túng Tâm Lý Mà Không Biết!"
        templates[0] = f"Vạch Trần Thủ Đoạn Thao Túng Đám Đông Tinh Vi"
        templates[1] = f"Nghệ Thuật Nhìn Thấu Lòng Người Qua Hành Vi Nhỏ"

    return t1, templates[:4]


def generate_marketing_meta(book: dict, shopee_link: str = None) -> dict:
    """
    Generate complete marketing package: Title, Alternatives, Debate Comment, Description, Hashtags.
    """
    slug = book.get("slug", "unknown")
    book_title = book.get("title", "Sách Hay").split("(")[0].strip()
    author = book.get("author", "Tác giả")
    core_msg = book.get("core_message", "")
    aff_link = shopee_link or f"{DEFAULT_AFF_BASE}/{slug}"

    if slug in CURATED_MARKETING_PACK:
        c = CURATED_MARKETING_PACK[slug]
        title_curiosity = c["title_curiosity"]
        alternative_titles = c["alternative_titles"]
        debate_q = c["debate_question"]
        callout = c["callout"]
    else:
        title_curiosity, alternative_titles = build_dynamic_titles(book_title, author, core_msg)
        debate_q = f"Bạn nghĩ sao về quan điểm: '{core_msg}'? Bạn có dám thừa nhận mình từng mắc phải sai lầm này không?"
        callout = f"Nếu bạn đang tìm kiếm câu trả lời cho những bế tắc trong cuộc sống, đây chính là cuốn sách bạn cần đọc sớm."

    # 1. PINNED COMMENT (Debate Hook + Shopee Affiliate)
    pinned_comment = (
        f"💬 {debate_q}\n\n"
        f"Hãy để lại góc nhìn của bạn bên dưới, cùng chia sẻ nhé! 👇\n\n"
        f"---\n"
        f"📖 Trích đoạn từ cuốn sách: {book_title} — {author}\n"
        f"👉 Link sách chính hãng mình đọc ở đây: {aff_link}\n"
        f"(Khuyên thật anh em nên mua bản chuẩn nhà xuất bản ở link này, đừng ham rẻ mua sách lậu in thiếu trang sai chữ nhé)."
    )

    # 2. SHORT COMMENT (Reply template)
    short_reply = (
        f"Dành cho bạn nào hỏi tên sách: Cuốn '{book_title}' của tác giả {author} nha! "
        f"Link sách chính hãng mình ghim ở bình luận đầu tiên và phần mô tả nhé. Chúc bạn đọc sách vui vẻ!"
    )

    # 3. DESCRIPTION (High SEO + Shopee CTA + Disclaimer)
    clean_tag = re.sub(r'[^a-zA-Z0-9]', '', slug)
    hashtags = f"#shorts #sachhay #radio2am #tuduy #trietlycuocsong #phattrienbanthan #{clean_tag}"

    description = (
        f"{title_curiosity}\n\n"
        f"{callout}\n"
        f"Cuốn sách '{book_title}' ({author}) vạch trần: {core_msg}\n\n"
        f"----------------\n"
        f"📌 MUA SÁCH CHÍNH HÃNG ỦNG HỘ TÁC GIẢ TẠI ĐÂY (SHOPEE MALL):\n"
        f"👉 Link Shopee: {aff_link}\n"
        f"(Áp dụng mã Freeship Extra & Voucher giảm giá độc quyền trong giỏ hàng)\n\n"
        f"----------------\n"
        f"🎙️ Kênh Radio 2AM — Nơi nói những sự thật mà ban ngày bạn không dám đối diện.\n"
        f"Bấm Đăng ký kênh để không bỏ lỡ các video thức tỉnh mỗi ngày!\n\n"
        f"{hashtags}"
    )

    return {
        "slug": slug,
        "book_title": book_title,
        "author": author,
        "title_curiosity": title_curiosity,
        "alternative_titles": alternative_titles,
        "pinned_comment": pinned_comment,
        "short_comment_reply": short_reply,
        "description": description,
        "hashtags": hashtags,
        "shopee_aff_link": aff_link
    }

