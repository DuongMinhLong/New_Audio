#!/usr/bin/env python3
"""
produce_book_photo_posts.py - Sản xuất trọn bộ Kịch bản Bài viết + Ảnh trích dẫn 4:5
cho 1 cuốn sách (4 phần thông tin đa chiều, chạm 4 góc nhìn tâm lý & đời sống).
Đồng bộ lưu vào Database riêng biệt: outputs/post_management.db
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from tools.post_db import add_or_update_post
from tools.post_image_generator import generate_quote_post_image

BOOK_SERIES_DATA = {
    "book_slug": "dam_bi_ghet",
    "book_title": "Dám Bị Ghét",
    "author": "Kishimi Ichiro & Koga Fumitake",
    "category": "Tâm Lý Học Adler & Bản Lĩnh Sống",
    "shopee_aff_link": "https://s.shopee.vn/9pfUrqKRhr",
    "hashtags": "#radio2am #dambighet #tamlyhocadler #thuctinh #tudonoitam #boclocuocsong",
    "parts": [
        {
            "part_number": 1,
            "slug": "dam_bi_ghet_phan1_people_pleaser",
            "part_title": "Phần 1: Nghịch Lý Làm Hài Lòng Thiên Hạ (Góc Nhìn Quan Hệ Xã Hội)",
            "sub_angle": "Bóc trần hội chứng người tốt giả tạo (People-pleaser): Càng sợ làm mất lòng người khác, bạn càng trở nên vô hình và bị bóc lột một cách hiển nhiên.",
            "badge_tag": "BẢN LĨNH TỪ CHỐI",
            "quote_on_image": "Càng cố gắng làm vừa lòng thiên hạ, bạn càng trở nên vô hình và bị bóc lột một cách hiển nhiên.",
            "caption": (
                "Điều tàn nhẫn nhất ở chốn công sở và các mối quan hệ: Kẻ luôn gật đầu trước mọi yêu cầu không phải là người được yêu quý, mà là kẻ đầu tiên bị lợi dụng.\n\n"
                "Từ bé, bạn được dạy phải ngoan ngoãn, biết nhường nhịn và không được làm phật lòng ai. Lớn lên, bạn biến thành một 'kẻ làm hài lòng người khác' chuyên nghiệp. Bạn sợ từ chối vì sợ bị đánh giá là ích kỷ. Bạn gánh thêm việc của đồng nghiệp, chịu đựng sự đòi hỏi vô lý của người thân, rồi đêm về nằm gặm nhấm sự kiệt sức một mình.\n\n"
                "Tâm lý học Adler trong 'Dám Bị Ghét' đập vỡ ảo tưởng này bằng một sự thật trần trụi:\n"
                "Nếu bạn sống chỉ để đáp ứng kỳ vọng của người khác, thì cuộc đời này rốt cuộc là của ai? Người khác chỉ quan tâm đến sự tiện lợi mà bạn mang lại, chứ không ai biết ơn sự hy sinh thầm lặng của bạn.\n\n"
                "Học cách nói 'KHÔNG' không phải là kiêu ngạo. Đó là phát súng đầu tiên bạn bắn ra để bảo vệ không gian sống và giá trị của chính mình.\n\n"
                "Trưởng thành thực sự bắt đầu từ ngày bạn dám nhìn thẳng vào mắt người khác và từ chối những điều làm tổn thương lòng tự trọng của bạn.\n\n"
                "📖 Tác phẩm: Dám Bị Ghét - Kishimi Ichiro & Koga Fumitake\n"
                "🛒 Mua sách chính hãng tại: https://s.shopee.vn/9pfUrqKRhr\n\n"
                "#radio2am #dambighet #peoplepleaser #banlinhsong #thuctinh #tamlyungdung"
            )
        },
        {
            "part_number": 2,
            "slug": "dam_bi_ghet_phan2_task_separation",
            "part_title": "Phần 2: Nghệ Thuật Phân Chia Nhiệm Vụ (Góc Nhìn Ranh Giới Cảm Xúc)",
            "sub_angle": "Kỹ thuật 'Tách biệt nhiệm vụ' của Alfred Adler: Dừng gánh vác rác cảm xúc, sự kỳ vọng và nỗi thất vọng của người khác để tìm lại tự do nội tâm.",
            "badge_tag": "RANH GIỚI THÉP",
            "quote_on_image": "Nửa đời sau của bạn sẽ thanh thản hơn rất nhiều, khi bạn hiểu việc người khác thất vọng về bạn... là chuyện của họ.",
            "caption": (
                "Lý do khiến đầu óc bạn luôn căng như dây đàn không phải vì núi công việc. Mà vì bạn đang vác trên vai gánh nặng cảm xúc của những người xung quanh.\n\n"
                "Sếp nhăn mặt, bạn thảng thốt nghĩ mình vừa phạm sai lầm gì. Bố mẹ so sánh bạn với con nhà người ta, bạn dằn vặt tự trách mình bất tài. Bạn sống như một chiếc ăng-ten thu nhận mọi tần số phán xét của thiên hạ.\n\n"
                "Adler chỉ cho bạn một chiếc chìa khóa giải thoát mang tên: 'Phân chia nhiệm vụ'.\n"
                "Quy tắc cực kỳ đơn giản: Khi đứng trước một vấn đề, hãy tự hỏi: Kết cục cuối cùng của chuyện này do ai gánh chịu? Ai là người phải trả giá cho lựa chọn đó?\n\n"
                "- Việc bạn sống tử tế, nỗ lực hết mình: Đó là nhiệm vụ của bạn.\n"
                "- Việc người ta có công nhận, có hài lòng hay quay lưng thất vọng: Đó là nhiệm vụ của họ.\n\n"
                "Can thiệp vào nhiệm vụ của người khác là căn nguyên của mọi bi kịch gia đình và công sở. Trả lại cho người khác trách nhiệm với cảm xúc của họ, và bạn sẽ thấy bầu trời tự do mở ra ngay lập tức.\n\n"
                "📖 Tác phẩm: Dám Bị Ghét - Kishimi Ichiro & Koga Fumitake\n"
                "🛒 Mua sách chính hãng tại: https://s.shopee.vn/9pfUrqKRhr\n\n"
                "#radio2am #dambighet #chiatachnhiemvu #ranhgioi #tudonoitam #adler"
            )
        }
        ,
        {
            "part_number": 3,
            "slug": "dam_bi_ghet_phan3_teleology_past",
            "part_title": "Phần 3: Cái Bẫy Đổ Lỗi Quá Khứ & Tuổi Thơ (Góc Nhìn Tâm Lý Học Hành Vi)",
            "sub_angle": "Mục đích luận (Teleology) bẻ gãy Thuyết nguyên nhân: Đừng mượn cớ tổn thương cũ làm tấm khiên hợp thức hóa việc trốn tránh nỗ lực thay đổi ở hiện tại.",
            "badge_tag": "BỎ TẤM KHIÊN QUÁ KHỨ",
            "quote_on_image": "Đừng lấy tổn thương quá khứ ra làm bình phong nữa. Bạn không hề bất lực, bạn chỉ đang sợ phải chịu trách nhiệm cho tương lai.",
            "caption": (
                "Bao nhiêu lần bạn tự nhủ: 'Vì tuổi thơ của tôi không trọn vẹn', 'Vì bố mẹ tôi độc hại', 'Vì tôi từng bị phản bội nên bây giờ tôi mới khép kín và thất bại'?\n\n"
                "Chúng ta rất thích bám vào quá khứ. Bởi vì đổ lỗi cho quá khứ là cách êm ái nhất để hợp thức hóa việc mình dậm chân tại chỗ. Nó cho bạn quyền đóng vai nạn nhân vô tội, được người đời thương hại mà không cần phải nỗ lực thay đổi.\n\n"
                "Nhưng triết lý Adler giáng một đòn chí mạng vào tâm lý này:\n"
                "Không có cái gọi là vết thương tâm lý quyết định tương lai của bạn. Chúng ta không chịu đau khổ vì cú sốc trong quá khứ, mà chúng ta tự tìm kiếm trong quá khứ những lý do phù hợp với MỤC ĐÍCH hiện tại của mình.\n\n"
                "Bạn nói bạn sợ giao tiếp vì từng bị bắt nạt? Sự thật là bạn chọn rút lui để không phải đối mặt với nguy cơ bị từ chối thêm lần nữa. Bạn dùng quá khứ làm tấm khiên chắn trước mặt mình.\n\n"
                "Quá khứ đã chết. Thứ duy nhất đang giam cầm bạn không phải là ngày hôm qua, mà là sự hèn nhát không dám bước ra khỏi vùng an toàn của ngày hôm nay.\n\n"
                "📖 Tác phẩm: Dám Bị Ghét - Kishimi Ichiro & Koga Fumitake\n"
                "🛒 Mua sách chính hãng tại: https://s.shopee.vn/9pfUrqKRhr\n\n"
                "#radio2am #dambighet #mucdichluan #khacphuctranhtap #thuctinh #tuduynguoc"
            )
        },
        {
            "part_number": 4,
            "slug": "dam_bi_ghet_phan4_courage_to_be_disliked",
            "part_title": "Phần 4: Dũng Khí Bị Ghét & Tự Do Đích Thực (Góc Nhìn Hiện Sinh & Hành Động)",
            "sub_angle": "Bản chất của tự do: Chấp nhận bị người khác ghét bỏ để bảo vệ bản sắc cá nhân và toàn tâm toàn ý sống trọn vẹn trong khoảnh khắc hiện tại.",
            "badge_tag": "DŨNG KHÍ TỰ DO",
            "quote_on_image": "Tự do đích thực không đến từ sự công nhận của số đông. Nó bắt đầu từ giây phút bạn dám bị kẻ khác ghét bỏ.",
            "caption": (
                "Cái giá đắt nhất của việc muốn được tất cả mọi người yêu quý là bạn phải sống một cuộc đời chắp vá theo tiêu chuẩn của người khác.\n\n"
                "Bạn chọn ngành học bố mẹ thích. Bạn mặc bộ đồ đồng nghiệp khen. Bạn nói những lời xã giao thảo mai để không ai mất lòng. Để rồi một ngày nhìn vào gương, bạn nhận ra người đứng trong đó hoàn toàn xa lạ.\n\n"
                "'Dám bị ghét' không phải là thái độ ngông cuồng hay bất cần đời. 'Dám bị ghét' là sự tỉnh táo tột cùng để nhận ra rằng: Dù bạn có hoàn hảo đến đâu, ngoài kia vẫn luôn có người ghét bạn vì một lý do ngớ ngẩn nào đó.\n\n"
                "Khi bạn không còn run sợ trước ánh mắt phán xét của đám đông, bạn mới thực sự chạm tay vào Tự Do.\n\n"
                "Tự do là được sống thật với giá trị của mình. Tự do là dũng cảm đi trên con đường mình đã chọn, dù hai bên đường có là tiếng vỗ tay hay tiếng la ó dè bỉu.\n\n"
                "Cuộc đời không phải là cuộc đua để lấy phiếu bầu yêu thích. Hãy sống sao cho đến phút cuối cùng, người duy nhất bạn không cảm thấy hổ thẹn chính là bản thân bạn.\n\n"
                "📖 Tác phẩm: Dám Bị Ghét - Kishimi Ichiro & Koga Fumitake\n"
                "🛒 Mua sách chính hãng tại: https://s.shopee.vn/9pfUrqKRhr\n\n"
                "#radio2am #dambighet #dungkhitudo #songbanchat #thuctinh #nhanban"
            )
        }

    ]
}


def produce_and_store_book():
    print("=" * 80)
    print(f"BẮT ĐẦU SẢN XUẤT 4 PHẦN BÀI VIẾT ĐA CHIỀU: {BOOK_SERIES_DATA['book_title'].upper()}")
    print("=" * 80)

    book_slug = BOOK_SERIES_DATA["book_slug"]
    book_title = BOOK_SERIES_DATA["book_title"]
    author = BOOK_SERIES_DATA["author"]
    category = BOOK_SERIES_DATA["category"]
    aff_link = BOOK_SERIES_DATA["shopee_aff_link"]
    hashtags = BOOK_SERIES_DATA["hashtags"]

    results = []
    for p in BOOK_SERIES_DATA["parts"]:
        part_num = p["part_number"]
        slug = p["slug"]
        part_title = p["part_title"]
        badge_tag = p["badge_tag"]
        quote_text = p["quote_on_image"]
        caption = p["caption"]
        sub_angle = p["sub_angle"]

        print(f"\n[PHẦN {part_num}/4] {part_title}")
        print(f"  • Góc nhìn: {sub_angle}")
        print(f"  • Badge Tag: [{badge_tag}]")
        print(f"  • Quote trên ảnh: \"{quote_text}\"")

        # 1. Tạo file ảnh 4:5
        img_filename = f"{slug}_4x5.png"
        img_path = generate_quote_post_image(
            quote_text=quote_text,
            book_title=book_title,
            author=author,
            badge_tag=badge_tag,
            output_filename=img_filename,
            ratio="4:5"
        )

        # 2. Lưu vào Database outputs/post_management.db
        post_record = {
            "slug": slug,
            "book_slug": book_slug,
            "book_title": book_title,
            "author": author,
            "category": category,
            "part_number": part_num,
            "part_title": part_title,
            "sub_angle": sub_angle,
            "badge_tag": badge_tag,
            "quote_on_image": quote_text,
            "caption": caption,
            "image_path": img_path,
            "shopee_aff_link": aff_link,
            "hashtags": hashtags,
            "upload_status": "CHƯA ĐĂNG"
        }
        post_id = add_or_update_post(post_record)
        print(f"  [OK] Đã lưu vào post_management.db (ID: {post_id}, Slug: {slug})")
        results.append(post_record)

    print("\n" + "=" * 80)
    print("TỔNG KẾT: ĐÃ HOÀN TẤT SẢN XUẤT 4 PHẦN ĐA CHIỀU CHO CUỐN SÁCH!")
    print("=" * 80)
    return results


if __name__ == "__main__":
    produce_and_store_book()

