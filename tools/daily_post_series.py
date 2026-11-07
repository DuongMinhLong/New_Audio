#!/usr/bin/env python3
"""
daily_post_series.py - Dữ liệu 12 Bài viết Facebook chuyên sâu kèm Ảnh (Photo Posts)
đồng bộ với 24 tập phim đang phát sóng trên Fanpage 2AM (15:30 mỗi ngày).
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DAILY_POSTS = [
    {
        "slug": "post_dam_bi_ghet_ngay1",
        "day_offset": 0,  # 06/11/2026 lúc 15:30
        "book_title": "Dám Bị Ghét",
        "author": "Kishimi Ichiro & Koga Fumitake",
        "badge_tag": "BẢN LĨNH SỐNG",
        "quote_on_image": "Tự do không phải là làm mọi điều mình thích. Tự do đích thực là khi bạn có đủ dũng khí để bị người khác ghét bỏ.",
        "caption": (
            "Điều tàn nhẫn nhất của cuộc đời là: Bạn có thể sống vừa lòng cả thiên hạ, rồi vẫn bị coi thường như một kẻ nhạt nhẽo.\n\n"
            "Chúng ta từ nhỏ đã bị dạy phải ngoan, phải làm hài lòng cha mẹ, thầy cô, rồi đến sếp và đối tác. Nhưng càng cố làm vừa lòng người khác, bạn càng đánh mất chính mình.\n\n"
            "Cuốn 'Dám Bị Ghét' chỉ ra một sự thật trần trụi:\n"
            "Ai đó ghét bạn, đó là việc của họ, không phải việc của bạn. Bạn không thể kiểm soát suy nghĩ của người khác.\n\n"
            "Dám bị ghét không phải là đi gây sự với thế giới. Đó là bản lĩnh dám sống đúng với giá trị của mình, dù cho số đông có lắc đầu.\n\n"
            "Trưởng thành bắt đầu từ khoảnh khắc bạn không còn cần sự công nhận của bất kỳ ai để cảm thấy mình có giá trị.\n\n"
            "📖 Tác phẩm: Dám Bị Ghét - Kishimi Ichiro & Koga Fumitake\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/9pfUrqKRhr\n\n"
            "#radio2am #dambighet #thuctinh #tudonoitam #boclocuocsong"
        )
    },
    {
        "slug": "post_dam_bi_ghet_ngay2",
        "day_offset": 1,  # 07/11/2026 lúc 15:30
        "book_title": "Dám Bị Ghét",
        "author": "Kishimi Ichiro & Koga Fumitake",
        "badge_tag": "TỰ DO NỘI TÂM",
        "quote_on_image": "Nửa đời sau của bạn sẽ thanh thản hơn rất nhiều... nếu bạn biết cách dừng gánh vác cảm xúc của người khác.",
        "caption": (
            "Lý do khiến bạn luôn kiệt sức không phải vì công việc nặng nhọc. Mà vì bạn đang ôm đồm rác cảm xúc của người khác.\n\n"
            "Ai đó nổi giận, bạn lo lắng xem mình đã làm sai điều gì. Ai đó buồn rầu, bạn tự thấy có lỗi nếu mình đang hạnh phúc.\n\n"
            "Tâm lý học Adler gọi phương pháp giải thoát này là: 'Chia tách nhiệm vụ'.\n\n"
            "Mỗi khi một vấn đề ập đến, hãy tự hỏi: Kết cục của việc này do ai gánh chịu? Nếu là họ, đó là nhiệm vụ của họ. Can thiệp vào việc của người khác là căn nguyên của mọi đau khổ và mâu thuẫn.\n\n"
            "Trả lại cho người khác trách nhiệm cuộc đời họ. Và giữ chặt lấy quyền tự do của chính mình.\n\n"
            "📖 Tác phẩm: Dám Bị Ghét - Kishimi Ichiro & Koga Fumitake\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/9pfUrqKRhr\n\n"
            "#radio2am #dambighet #chiatachnhiemvu #thuctinh #tudonoitam"
        )
    },
    {
        "slug": "post_tam_ly_hoc_ve_tien_ngay3",
        "day_offset": 2,  # 08/11/2026 lúc 15:30
        "book_title": "Tâm Lý Học Về Tiền",
        "author": "Morgan Housel",
        "badge_tag": "TƯ DUY TIỀN BẠC",
        "quote_on_image": "Tiêu tiền để chứng minh cho người khác thấy mình có tiền... là cách nhanh nhất để bạn trở nên khánh kiệt.",
        "caption": (
            "Nghịch lý lớn nhất của người trẻ hiện đại: Mua những thứ mình không cần, bằng số tiền mình chưa làm ra, để gây ấn tượng với những kẻ mình chẳng hề thích.\n\n"
            "Cuốn 'Tâm Lý Học Về Tiền' của Morgan Housel phân biệt rõ hai khái niệm:\n"
            "- Giàu có bề nổi (Rich): Là mức thu nhập và những món đồ bạn phô trương ra ngoài (xe sang, đồ hiệu, check-in sang chảnh).\n"
            "- Thịnh vượng đích thực (Wealth): Là những tài sản bạn chưa chi tiêu. Là số tiền tích lũy cho bạn quyền năng nói 'KHÔNG' với những thứ bạn căm ghét.\n\n"
            "Đừng để bẫy tiêu dùng của mạng xã hội biến bạn thành nô lệ của những khoản nợ tín dụng.\n\n"
            "📖 Tác phẩm: Tâm Lý Học Về Tiền - Morgan Housel\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/9zyv49JoMu\n\n"
            "#radio2am #tamlyhocvetien #morganhousel #thuctinhtaichinh #tudotaichinh"
        )
    },
    {
        "slug": "post_tam_ly_hoc_ve_tien_ngay4",
        "day_offset": 3,  # 09/11/2026 lúc 15:30
        "book_title": "Tâm Lý Học Về Tiền",
        "author": "Morgan Housel",
        "badge_tag": "TỰ DO TÀI CHÍNH",
        "quote_on_image": "Giá trị cao nhất của tiền bạc không phải là mua được đồ xa xỉ. Mà là cho bạn quyền thức dậy mỗi sáng và tự quyết định ngày hôm nay mình làm gì.",
        "caption": (
            "Bạn có bao giờ tự hỏi: Mục đích cuối cùng của việc kiếm tiền là gì?\n\n"
            "Nhiều người nghĩ đó là nhà to, xe sang, danh phận. Nhưng khi đạt được rồi, họ nhận ra sự trống rỗng vẫn ở đó, chỉ có hóa đơn bảo dưỡng là tăng lên.\n\n"
            "Đỉnh cao của tiền bạc là Tự Do Thời Gian.\n\n"
            "Có tiền để không phải cúi đầu trước một môi trường độc hại. Có tiền để dành thời gian cho cha mẹ già, con cái nhỏ mà không nơm nớp lo mất việc. Có tiền để khi biến cố ập đến, bạn có quyền bình tĩnh lựa chọn thay vì tuyệt vọng.\n\n"
            "Tiền bạc là công cụ mua lại quyền làm chủ thời gian. Đừng đánh đổi ngược lại toàn bộ đời mình chỉ để tích lũy những thứ đồ chơi hào nhoáng.\n\n"
            "📖 Tác phẩm: Tâm Lý Học Về Tiền - Morgan Housel\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/9zyv49JoMu\n\n"
            "#radio2am #tamlyhocvetien #tudothoigian #thuctinh #songbanchat"
        )
    }
    ,
    {
        "slug": "post_atomic_habits_ngay5",
        "day_offset": 4,  # 10/11/2026 lúc 15:30
        "book_title": "Atomic Habits",
        "author": "James Clear",
        "badge_tag": "KỶ LUẬT BẢN THÂN",
        "quote_on_image": "Bạn không vươn lên tới tầm của mục tiêu. Bạn sẽ rơi xuống bằng đúng trình độ của hệ thống thói quen bạn làm mỗi ngày.",
        "caption": (
            "Ai cũng muốn thành công, giảm cân, giàu có. Nhưng tại sao 95% thất bại sau 2 tuần hừng hực khí thế?\n\n"
            "Bởi vì bạn đang rơi vào 'Bẫy Mục Tiêu'.\n\n"
            "James Clear trong 'Atomic Habits' chỉ ra: Kẻ thắng và người thua đều có chung mục tiêu. Thứ phân định kẻ thắng cuộc là HỆ THỐNG thực thi.\n\n"
            "Đừng chỉ dựa vào ý chí hay động lực nhất thời. Động lực là thứ rẻ tiền nhất, nó đến rồi đi sau một giấc ngủ.\n\n"
            "Hãy thiết kế môi trường sao cho thói quen tốt trở nên hiển nhiên và thói quen xấu trở nên khó khăn. Kỷ luật thép được xây dựng từ những thay đổi 1% cực nhỏ nhưng bền bỉ qua năm tháng.\n\n"
            "📖 Tác phẩm: Atomic Habits (Thay Đổi Tí Hon) - James Clear\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/AAILGSJB1x\n\n"
            "#radio2am #atomichabits #jamesclear #kyluatbathan #thaydoitohon"
        )
    },
    {
        "slug": "post_atomic_habits_ngay6",
        "day_offset": 5,  # 11/11/2026 lúc 15:30
        "book_title": "Atomic Habits",
        "author": "James Clear",
        "badge_tag": "LÃI KÉP HÀNH VI",
        "quote_on_image": "Mỗi hành động bạn làm trong ngày hôm nay... là một lá phiếu bạn bầu cho con người mà bạn muốn trở thành.",
        "caption": (
            "Nằm lướt TikTok thêm 1 tiếng, hay mở một trang sách đọc?\n"
            "Ăn thêm một gói snack đêm khuya, hay xỏ giày chạy bộ?\n\n"
            "Một hành động đơn lẻ dường như chẳng thay đổi cuộc đời bạn ngay lập tức. Đó là lý do chúng ta dễ dãi thỏa hiệp với sự lười biếng.\n\n"
            "Nhưng hãy nhớ: Thói quen là lãi kép của sự tự hoàn thiện. Giống như tiền sinh lời qua lãi kép, tác động của thói quen nhân lên gấp bội khi thời gian trôi qua.\n\n"
            "Bạn không cần trở nên vĩ đại ngay hôm nay. Hãy bắt đầu từ việc tốt hơn 1% so với ngày hôm qua. Sau 1 năm, bạn sẽ tiến bộ gấp 37 lần.\n\n"
            "📖 Tác phẩm: Atomic Habits (Thay Đổi Tí Hon) - James Clear\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/AAILGSJB1x\n\n"
            "#radio2am #atomichabits #laikep #thuctinh #thoiqtot"
        )
    },
    {
        "slug": "post_dac_nhan_tam_ngay7",
        "day_offset": 6,  # 12/11/2026 lúc 15:30
        "book_title": "Đắc Nhân Tâm",
        "author": "Dale Carnegie",
        "badge_tag": "ỨNG XỬ THỰC CHIẾN",
        "quote_on_image": "Kẻ thắng trong một cuộc tranh cãi thường là kẻ thua trong mối quan hệ. Đừng đánh đổi danh dự người khác để thỏa mãn cái tôi của mình.",
        "caption": (
            "Cãi thắng một cuộc tranh luận thì sao? Bạn được hả hê trong vài phút, nhưng bạn đã vĩnh viễn đánh mất sự tôn trọng và tình cảm của đối phương.\n\n"
            "Dale Carnegie đã đúc kết trong 'Đắc Nhân Tâm':\n"
            "Cách duy nhất để chiến thắng trong một cuộc tranh cãi là... TRÁNH NÓ.\n\n"
            "Khi bạn dồn người khác vào chân tường, ép họ phải nhận sai trước mặt đám đông, lòng tự ái của họ sẽ biến thành sự thù địch ngấm ngầm.\n\n"
            "Người có bản lĩnh không cần phải chứng minh mình luôn đúng. Họ biết nhường bước ở những chuyện vụn vặt để gìn giữ những mục tiêu lớn hơn.\n\n"
            "📖 Tác phẩm: Đắc Nhân Tâm - Dale Carnegie\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/9fM4fXL52o\n\n"
            "#radio2am #dacnhantam #dalecarnegie #giaotiep #boclocuocsong"
        )
    },
    {
        "slug": "post_dac_nhan_tam_ngay8",
        "day_offset": 7,  # 13/11/2026 lúc 15:30
        "book_title": "Đắc Nhân Tâm",
        "author": "Dale Carnegie",
        "badge_tag": "RANH GIỚI TỬ TẾ",
        "quote_on_image": "Lòng tốt mà không có ranh giới và răng nanh... thì chẳng khác nào sự phục tùng hèn nhát.",
        "caption": (
            "Nhiều người đọc Đắc Nhân Tâm rồi biến mình thành một kẻ thảo mai luôn mỉm cười gật đầu với tất cả mọi người.\n\n"
            "Đó là sai lầm chết người.\n\n"
            "Tử tế khác với hèn nhát. Chân thành khác với xu nịnh. Nếu bạn đối tốt với ai đó chỉ vì sợ bị họ ghét bỏ, họ sẽ không tôn trọng bạn, mà sẽ coi lòng tốt của bạn là điều hiển nhiên.\n\n"
            "Một người trưởng thành đích thực luôn có lòng trắc ẩn ấm áp, nhưng đi kèm với một ranh giới thép không ai được phép vượt qua.\n\n"
            "Hãy sống tử tế, nhưng hãy nhớ giữ lại chút gai góc để tự bảo vệ chính mình.\n\n"
            "📖 Tác phẩm: Đắc Nhân Tâm - Dale Carnegie\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/9fM4fXL52o\n\n"
            "#radio2am #dacnhantam #ranhgioi #longtotbannhanh #thuctinh"
        )
    }

    ,
    {
        "slug": "post_deep_work_ngay9",
        "day_offset": 8,  # 14/11/2026 lúc 15:30
        "book_title": "Deep Work",
        "author": "Cal Newport",
        "badge_tag": "SỨC MẠNH TẬP TRUNG",
        "quote_on_image": "Kẻ nghiện dopamine ngắn sẽ làm việc cho kẻ có khả năng ngồi yên tập trung sâu trong hai giờ đồng hồ.",
        "caption": (
            "Não của bạn có đang bị 'sương mù não' (Brain Rot)?\n\n"
            "Mỗi 3 phút lại mở điện thoại kiểm tra thông báo. Không thể đọc hết một bài viết dài. Vừa làm việc vừa mở 15 tab trình duyệt.\n\n"
            "Cal Newport trong cuốn 'Deep Work' cảnh báo: Khả năng tập trung sâu đang trở thành một siêu năng lực hiếm có trong thời đại kinh tế số.\n\n"
            "Những công việc nông cạn, vụn vặt sẽ bị AI thay thế đầu tiên. Thứ duy nhất bảo vệ giá trị và mức thu nhập của bạn là năng lực giải quyết các bài toán hóc búa đòi hỏi sự chú ý tuyệt đối.\n\n"
            "Tập trung không phải là bẩm sinh. Đó là một cơ bắp. Càng buông thả lướt short video, cơ bắp đó càng teo tóp.\n\n"
            "📖 Tác phẩm: Deep Work (Làm Việc Sâu) - Cal Newport\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/5q9M6UZfpD\n\n"
            "#radio2am #deepwork #calnewport #taptrungsau #suongmunao"
        )
    },
    {
        "slug": "post_deep_work_ngay10",
        "day_offset": 9,  # 15/11/2026 lúc 15:30
        "book_title": "Deep Work",
        "author": "Cal Newport",
        "badge_tag": "BẢN LĨNH CÔNG NGHỆ",
        "quote_on_image": "Nếu bạn không chủ động lên kế hoạch cho sự chú ý của mình... các thuật toán mạng xã hội sẽ làm điều đó thay bạn.",
        "caption": (
            "Hàng ngàn kỹ sư hàng đầu thế giới ở Thung lũng Silicon đang ngày đêm tối ưu hóa thuật toán chỉ với một mục đích: Cướp đoạt từng giây sự chú ý của bạn.\n\n"
            "Và phần lớn chúng ta đang tự nguyện dâng nộp bộ não của mình miễn phí.\n\n"
            "Người làm việc sâu (Deep Worker) không chạy theo mọi tiếng 'ting ting' của thông báo. Họ xây dựng một pháo đài cô lập: Tắt thông báo, đóng cửa phòng, và làm việc với cường độ cao trong 90 phút.\n\n"
            "Bớt một giờ lướt mạng vô nghĩa là thêm một giờ tạo ra giá trị đột phá cho cuộc đời bạn.\n\n"
            "📖 Tác phẩm: Deep Work (Làm Việc Sâu) - Cal Newport\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/5q9M6UZfpD\n\n"
            "#radio2am #deepwork #cainhiendopamine #nangsuat #thuctinh"
        )
    },
    {
        "slug": "post_cant_hurt_me_ngay11",
        "day_offset": 10,  # 16/11/2026 lúc 15:30
        "book_title": "Can't Hurt Me",
        "author": "David Goggins",
        "badge_tag": "Ý CHÍ THÉP",
        "quote_on_image": "Khi tâm trí bạn gào lên rằng bạn đã kiệt sức và muốn bỏ cuộc... Thực chất bạn mới chỉ dùng hết 40% công lực của mình.",
        "caption": (
            "Hầu hết chúng ta sống cả đời mà chưa từng một lần chạm đến giới hạn thực sự của bản thân.\n\n"
            "Bộ não con người có cơ chế sinh tồn tự nhiên: Khi gặp một chút đau đớn, khó khăn hay mệt mỏi, nó sẽ kích hoạt nút hãm phanh để bảo vệ bạn trong vùng an toàn.\n\n"
            "David Goggins gọi đây là 'Quy Tắc 40%'.\n\n"
            "Những người vĩ đại không phải là những người không biết mệt. Họ chỉ là những người biết cách đàm phán với tiếng nói hèn nhát trong đầu để bước tiếp qua rào cản 40% đó.\n\n"
            "Bạn mạnh mẽ hơn rất nhiều so với những gì bạn tự huyễn hoặc về chính mình.\n\n"
            "📖 Tác phẩm: Can't Hurt Me - David Goggins\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/AKblSlIXh0\n\n"
            "#radio2am #canthurtme #davidgoggins #quytac40 #ychithep"
        )
    },
    {
        "slug": "post_cant_hurt_me_ngay12",
        "day_offset": 11,  # 17/11/2026 lúc 15:30
        "book_title": "Can't Hurt Me",
        "author": "David Goggins",
        "badge_tag": "TÂM TRÍ CHAI SẠN",
        "quote_on_image": "Đừng cầu mong một cuộc đời dễ dãi. Hãy rèn luyện để có một tâm trí chai sạn trước mọi nghịch cảnh.",
        "caption": (
            "Hơi một chút áp lực là xin nghỉ việc 'để chữa lành'.\n"
            "Hơi một chút thất bại là ngồi dằn vặt oán trách số phận.\n\n"
            "Sự thật là: Cuộc đời này không quan tâm bạn bị tổn thương thế nào. Thế giới ngoài kia sẽ không dịu dàng hơn chỉ vì bạn yếu đuối.\n\n"
            "Thứ duy nhất giúp bạn đứng vững giữa giông bão là một 'Tâm Trí Chai Sạn' (Calloused Mind) — giống như bàn tay nâng tạ nhiều năm chai cứng trước gai nhọn.\n\n"
            "Mỗi lần bạn chọn thức dậy sớm khi trời lạnh, mỗi lần bạn không bỏ cuộc giữa chừng, bạn đang đóng thêm một lớp giáp thép cho tâm trí mình.\n\n"
            "Đừng chờ đợi phép màu. Hãy tự biến mình thành điểm tựa vững chãi nhất của chính mình.\n\n"
            "📖 Tác phẩm: Can't Hurt Me - David Goggins\n"
            "🛒 Mua sách chính hãng tại: https://s.shopee.vn/AKblSlIXh0\n\n"
            "#radio2am #canthurtme #tamtrichaisan #thuctinh #chualanhthat"
        )
    }

]
