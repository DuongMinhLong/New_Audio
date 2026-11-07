#!/usr/bin/env python3
"""
multi_series_metadata.py - Metadata and scene queries for Multi-Part Book Series Pilot
Top 3 books x 4 episodes = 12 episodes total.
"""

PILOT_SERIES = [
    {
        "series_slug": "dam_bi_ghet",
        "book_title": "Dám Bị Ghét",
        "author": "Ichiro Kishimi & Fumitake Koga",
        "category": "Tâm Lý & Phát Triển Bản Thân",
        "shopee_aff_link": "https://s.shopee.vn/9pfUrqKRhr",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú Tát Thức Tỉnh: Ảo Tưởng Làm Hài Lòng Tất Cả (People-Pleaser)",
                "pain_focus": "Hội chứng sợ bị ghét; gồng mình nhẫn nhịn sống theo kỳ vọng của thiên hạ để rồi bị coi thường, bóc lột và cô độc.",
                "hook_seed": "Càng cố gắng sống tử tế để được tất cả mọi người yêu quý... Bạn càng trở thành một kẻ vô hình đáng thương!",
                "cliffhanger": "Nhưng nếu dám từ chối, làm sao để bạn không biến mình thành kẻ ích kỷ và bị cô lập? Bí mật nằm ở Tập 2...",
                "scenes": [
                    {"query": "stressed office worker smiling painfully colleague conversation", "duration": 6.0},
                    {"query": "person sighing heavily holding temples exhaustion dark office", "duration": 6.5},
                    {"query": "lonely figure walking under street lamp quiet rain night", "duration": 5.5},
                    {"query": "clock ticking rapidly empty meeting room late night", "duration": 6.0},
                    {"query": "person looking at phone messages unread anxious face", "duration": 6.5},
                    {"query": "shadow puppet strings pulling tired puppet silhouette", "duration": 5.5},
                    {"query": "deep thoughtful breath looking into city neon lights", "duration": 6.0},
                    {"query": "standing up firmly pushing chair back leaving table", "duration": 6.5},
                    {"query": "calm determined face walking through crowded train station", "duration": 6.0},
                    {"query": "man standing alone on urban high rise rooftop sunset", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh Giới Thép: Kỹ Thuật Phân Chia Nhiệm Vụ Adler",
                "pain_focus": "Áp lực từ sự kỳ vọng của bố mẹ, sếp; ôm đồm cảm xúc của người khác; không dám nói 'KHÔNG'.",
                "hook_seed": "Làm vừa lòng sếp hay bố mẹ... KHÔNG PHẢI VIỆC CỦA BẠN!",
                "cliffhanger": "Nhưng lý do sâu xa khiến bạn không dám dựng ranh giới thép... lại nằm ở một cái cớ mà bạn giấu kín suốt nhiều năm qua — sự thật ở Tập 3...",
                "scenes": [
                    {"query": "chalk line drawn firmly on dark asphalt ground macro", "duration": 6.0},
                    {"query": "hand firmly gesturing stop barrier to camera", "duration": 6.0},
                    {"query": "heavy wooden door closing firmly shut lock clicking", "duration": 6.5},
                    {"query": "confident person walking away from chaotic argue office", "duration": 6.0},
                    {"query": "tearing up overwhelming task checklist calm resolve", "duration": 5.5},
                    {"query": "person drinking hot tea quietly by window raining", "duration": 6.5},
                    {"query": "breaking iron chains macro slow motion conceptual", "duration": 6.0},
                    {"query": "unbothered person working deeply on laptop dark room", "duration": 6.5},
                    {"query": "wise calm smile looking into camera steady posture", "duration": 6.0},
                    {"query": "walking forward with quiet confidence empty autumn park", "duration": 6.5}
                ]
            },
            {
                "episode": 3,
                "sub_angle": "Bóc Trần Mặt Tối: Cái Bẫy Đổ Lỗi Quá Khứ & Tuổi Thơ",
                "pain_focus": "Lấy cớ 'tuổi thơ bất hạnh', 'gia đình độc hại' để hợp thức hóa sự lười biếng và hèn nhát không dám thay đổi (Mục đích luận Adler).",
                "hook_seed": "Đừng mượn cớ tổn thương tuổi thơ nữa... Bạn không hề bất lực... Bạn chỉ đang dùng quá khứ làm TẤM KHIÊN để lười thay đổi!",
                "cliffhanger": "Khi không còn quá khứ để đổ lỗi, vũ khí duy nhất để bạn làm chủ cuộc đời mình là gì? Lời giải ở Tập 4...",
                "scenes": [
                    {"query": "burning old faded vintage photograph flames ash", "duration": 6.0},
                    {"query": "person looking at cracked shattered glass reflection dark", "duration": 6.5},
                    {"query": "tearing old paper notebook pages slow motion", "duration": 5.5},
                    {"query": "heavy rain storm hitting window glass moody night", "duration": 6.0},
                    {"query": "person washing face cold water bathroom mirror intense", "duration": 6.5},
                    {"query": "stepping boldly across dark boundary line floor", "duration": 6.0},
                    {"query": "standing tall facing turbulent storm clouds head on", "duration": 6.5},
                    {"query": "sharp focused gaze directly into camera determination", "duration": 6.0},
                    {"query": "golden sunlight breaking through dark storm clouds", "duration": 6.0},
                    {"query": "silhouette walking toward rising sun mountain ridge", "duration": 6.5}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn Bẩy Tự Do: Dũng Khí Sống Ở Hiện Tại & Dám Bị Ghét",
                "pain_focus": "Nỗi sợ tương lai vô định; dằn vặt vì quá khứ; tự do thực sự là bản lĩnh chấp nhận bị người khác ghét để sống đúng bản chất của mình.",
                "hook_seed": "Tự do đích thực của một con người... bắt đầu từ giây phút bạn DÁM BỊ KẺ KHÁC GHÉT BỎ!",
                "cliffhanger": "Hãy xem lại từ Tập 1 để hiểu trọn vẹn triết lý này, và cuốn sách gốc đang chờ bạn ở bình luận ghim.",
                "scenes": [
                    {"query": "person standing bold high above city rooftop horizon", "duration": 6.5},
                    {"query": "deep calm breath overlooking misty mountain landscape", "duration": 6.0},
                    {"query": "walking confidently against fast moving crowd blur", "duration": 6.5},
                    {"query": "candid genuine smile of inner freedom looking up sky", "duration": 6.0},
                    {"query": "open hands letting sand fly into warm breeze ocean", "duration": 5.5},
                    {"query": "closing heavy old book with satisfying quiet thud", "duration": 6.0},
                    {"query": "lighting single glowing candle in pitch dark room", "duration": 6.0},
                    {"query": "walking along ocean coast golden sunset warm sunlight", "duration": 6.5},
                    {"query": "calm steady footsteps forward clean modern walkway", "duration": 6.0},
                    {"query": "silhouette looking into vast golden horizon dusk", "duration": 6.5}
                ]
            }

        ]
    },
    {
        "series_slug": "tam_ly_hoc_ve_tien",
        "book_title": "Tâm Lý Học Về Tiền",
        "author": "Morgan Housel",
        "category": "Tài Chính & Tư Duy Tiền Bạc",
        "shopee_aff_link": "https://s.shopee.vn/9zyv49JoMu",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú Tát Thức Tỉnh: Bẫy Phông Bạt & Nợ Tín Dụng Mua Trước Trả Sau",
                "pain_focus": "Tiêu tiền chưa làm ra để mua thứ không cần nhằm gây ấn tượng với kẻ mình ghét; bẫy nợ BNPL và kiệt quệ tài chính.",
                "hook_seed": "Tiêu tiền để chứng minh mình có tiền... là cách NHANH NHẤT để bạn cạn kiệt tiền!",
                "cliffhanger": "Nhưng tại sao ngay cả những người kiếm được hàng trăm triệu vẫn không bao giờ thấy an tâm? Bí mật ở Tập 2...",
                "scenes": [
                    {"query": "shiny luxury sports car driving night neon reflections", "duration": 6.0},
                    {"query": "tapping credit card on pos payment terminal glowing", "duration": 5.5},
                    {"query": "exhausted person checking negative balance phone dark room", "duration": 6.5},
                    {"query": "person scrolling online shopping app late night bed", "duration": 6.0},
                    {"query": "money notes falling down in slow motion darkness", "duration": 6.0},
                    {"query": "person holding head in hands stressed bills desk", "duration": 6.5},
                    {"query": "expensive champagne glass bubble party fake laugh", "duration": 5.5},
                    {"query": "walking alone empty city street neon signs flickering", "duration": 6.0},
                    {"query": "throwing away flashy shopping bag calm realization", "duration": 6.5},
                    {"query": "staring into rain on window contemplation minimalist", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Bi Kịch Không Bao Giờ Thấy 'ĐỦ': Cột Mốc Di Chuyển",
                "pain_focus": "Lòng tham và so bì khiến cột mốc 'đủ' liên tục dịch chuyển xa hơn; cày kiệt sức 14 tiếng mỗi ngày nhưng lo âu không dứt.",
                "hook_seed": "Bi kịch lớn nhất của tiền bạc là... Càng kiếm được nhiều, bạn càng không bao giờ thấy ĐỦ!",
                "cliffhanger": "Nhưng đừng vội tự trách mình kém cỏi, vì thành công của những người bạn đang ghen tị... có một sự thật trần trụi ở Tập 3...",
                "scenes": [
                    {"query": "person running endlessly inside hamster wheel metaphor", "duration": 6.0},
                    {"query": "stack of gold coins building high and tumbling down", "duration": 6.0},
                    {"query": "exhausted office worker rubbing eyes 22h dark office", "duration": 6.5},
                    {"query": "comparing social media wealth posts jealous side eye", "duration": 6.0},
                    {"query": "deep sigh taking off luxury watch placing on table", "duration": 6.0},
                    {"query": "still calm lake surface early morning fog reflection", "duration": 6.5},
                    {"query": "man writing simple budget in notebook peaceful light", "duration": 5.5},
                    {"query": "closing laptop with quiet relief at evening sunset", "duration": 6.5},
                    {"query": "warm cup of tea held in hands simple living", "duration": 6.0},
                    {"query": "sitting on wooden porch enjoying quiet garden breeze", "duration": 6.5}
                ]
            },
            {
                "episode": 3,
                "sub_angle": "Bóc Trần Mặt Tối: Nghịch Lý May Mắn & Rủi Ro",
                "pain_focus": "Sùng bái mù quáng những tấm gương tỷ phú mà quên mất 80% kết quả là do ngẫu nhiên và may mắn; đánh đồng thành công với tài năng.",
                "hook_seed": "Đừng vội sùng bái những kẻ giàu có trên mạng! Tám mươi phần trăm thành công đó... chỉ là sự MAY MẮN NGẪU NHIÊN!",
                "cliffhanger": "Vậy nếu may mắn là thứ không kiểm soát được, đâu là giá trị duy nhất đồng tiền có thể mang lại cho bạn? Câu trả lời ở Tập 4...",
                "scenes": [
                    {"query": "pair of white dice rolling slow motion wooden table", "duration": 6.0},
                    {"query": "stock market red crash candles chart screen falling", "duration": 6.0},
                    {"query": "massive ocean wave crashing against lighthouse storm", "duration": 6.5},
                    {"query": "calm captain holding ship wheel steady through tempest", "duration": 6.5},
                    {"query": "person holding black umbrella standing strong in downpour", "duration": 6.0},
                    {"query": "drawing clear safety margin line in sketchbook desk", "duration": 5.5},
                    {"query": "stacking emergency cash neatly inside safe drawer", "duration": 6.0},
                    {"query": "steady mindful gaze looking out train window travel", "duration": 6.5},
                    {"query": "autumn leaves falling in quiet park solitary walk", "duration": 6.0},
                    {"query": "mountain summit standing tall above swirling clouds", "duration": 6.5}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn Bẩy Tự Do: Lợi Tức Cao Nhất Của Đồng Tiền: Sự Tự Do",
                "pain_focus": "Giá trị tối thượng của tiền không phải mua sắm phô trương, mà là quyền kiểm soát thời gian — thức dậy mỗi sáng và làm điều mình muốn.",
                "hook_seed": "Giá trị lớn nhất của đồng tiền... KHÔNG PHẢI là mua nhà hay đổi xe!",
                "cliffhanger": "Hãy xem lại từ Tập 1 để cài đặt lại tư duy tài chính của bạn, và cuốn sách gốc đang nằm ở bình luận ghim.",
                "scenes": [
                    {"query": "waking up naturally in sunlight bedroom stretch calm", "duration": 6.5},
                    {"query": "sipping morning coffee looking out serene green forest", "duration": 6.0},
                    {"query": "closing laptop stepping outside into nature sunlight", "duration": 6.0},
                    {"query": "walking freely through autumn forest leaves peaceful path", "duration": 6.5},
                    {"query": "father playing happily with young child in park green", "duration": 6.0},
                    {"query": "reading book in cozy hammock under warm sun rays", "duration": 6.0},
                    {"query": "looking at open calendar with completely free schedule", "duration": 5.5},
                    {"query": "standing on ocean cliff watching sunset peaceful breath", "duration": 6.5},
                    {"query": "smiling quietly with total peace of mind urban cafe", "duration": 6.0},
                    {"query": "walking toward golden horizon sun slow motion free", "duration": 6.5}
                ]
            }

        ]
    }
    ,
    {
        "series_slug": "atomic_habits",
        "book_title": "Atomic Habits (Thay Đổi Tí Hon)",
        "author": "James Clear",
        "category": "Kỷ Luật & Năng Suất",
        "shopee_aff_link": "https://s.shopee.vn/AAILGSJB1x",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú Tát Thức Tỉnh: Ảo Tưởng Ý Chí & Cái Bẫy Trì Hoãn Tích Lũy",
                "pain_focus": "Tin vào động lực nhất thời, chờ cảm hứng mới làm; xem thường sự hủy diệt âm thầm của thói quen xấu tí hon tích lũy mỗi ngày.",
                "hook_seed": "Bạn không thất bại vì thiếu ý chí! Bạn thất bại vì cái bẫy động lực đang RU NGỦ bạn mỗi ngày!",
                "cliffhanger": "Vậy tại sao càng cố gắng gồng mình kỷ luật, bạn càng nhanh bỏ cuộc? Bí mật nằm ở môi trường sống ở Tập 2...",
                "scenes": [
                    {"query": "alarm clock ringing hand hitting snooze button 6am", "duration": 5.5},
                    {"query": "scrolling phone in dark bed guilty anxious face", "duration": 6.5},
                    {"query": "cluttered chaotic desk messy papers spilled coffee", "duration": 6.0},
                    {"query": "macro dominoes falling one by one chain reaction", "duration": 6.0},
                    {"query": "hourglass sand slipping fast through glass macro", "duration": 5.5},
                    {"query": "tired person staring blankly at glowing laptop screen", "duration": 6.5},
                    {"query": "water dripping steadily eroding stone block macro", "duration": 6.0},
                    {"query": "person rubbing tired face in bathroom mirror midnight", "duration": 6.0},
                    {"query": "taking a deep breath sitting up straight on chair", "duration": 6.0},
                    {"query": "writing a single clean checkmark on calendar page", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh Giới Thực Chiến: Thiết Kế Môi Trường Sống (Environment Design)",
                "pain_focus": "Chiến đấu với cám dỗ bằng ý chí là tự sát; kẻ có kỷ luật thép nhất thực chất là người ít phải dùng đến ý chí nhất nhờ thiết kế môi trường.",
                "hook_seed": "Người có kỷ luật thép... KHÔNG HỀ có ý chí mạnh hơn bạn!",
                "cliffhanger": "Nhưng thiết kế môi trường mới chỉ là một nửa cuộc chơi, sai lầm chết người nhất của người thất bại... lại nằm ở cách đặt mục tiêu ở Tập 3...",
                "scenes": [
                    {"query": "putting smartphone inside wooden drawer locking key away", "duration": 6.0},
                    {"query": "clean minimalist desk setup morning sunlight quiet room", "duration": 6.5},
                    {"query": "throwing away junk food snacks into trash bin kitchen", "duration": 5.5},
                    {"query": "placing clean running shoes right next to front door", "duration": 6.0},
                    {"query": "organizing bookshelf books neatly in quiet study", "duration": 6.0},
                    {"query": "focused deep work session laptop no notifications", "duration": 6.5},
                    {"query": "filling glass bottle with fresh water on tidy table", "duration": 5.5},
                    {"query": "satisfied smile closing laptop at 17h productive day", "duration": 6.5},
                    {"query": "turning off overhead bright lights leaving tidy workspace", "duration": 6.0},
                    {"query": "peaceful evening walk in quiet neighborhood sunset", "duration": 6.5}
                ]
            },
            {
                "episode": 3,
                "sub_angle": "Bóc Trần Mặt Tối: Nghịch Lý Mục Tiêu vs Hệ Thống (Goals vs Systems)",
                "pain_focus": "Người chiến thắng và kẻ thất bại đều có cùng một mục tiêu; đặt mục tiêu chỉ cho ta hướng đi, chỉ có hệ thống vận hành hàng ngày mới mang lại kết quả.",
                "hook_seed": "Đặt mục tiêu cho năm mới... là trò lừa đảo lớn nhất mà bạn tự vẽ ra!",
                "cliffhanger": "Vậy đâu mới là điểm tựa vững chắc nhất để thói quen tự vận hành suốt đời? Đón xem Tập 4...",
                "scenes": [
                    {"query": "writing ambitious goals list in notebook with enthusiasm", "duration": 6.0},
                    {"query": "striking through unaccomplished goals in frustration", "duration": 6.0},
                    {"query": "complex brass gears turning smoothly clockwork mechanism", "duration": 6.5},
                    {"query": "athlete tying laces practicing alone in empty dawn track", "duration": 6.5},
                    {"query": "consistent steady pushups floor sweat dripping focus", "duration": 6.0},
                    {"query": "stopwatch ticking steady rhythmic seconds hand macro", "duration": 5.5},
                    {"query": "hands typing steadily code text on keyboard flow state", "duration": 6.0},
                    {"query": "carpenter carefully smoothing wood plank with hand plane", "duration": 6.5},
                    {"query": "calm determined expression looking straight at horizon", "duration": 6.0},
                    {"query": "standing victorious after long grueling mountain hike", "duration": 6.5}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn Bẩy Tự Do: Thay Đổi Căn Tính Bản Thân (Identity-Based Habits)",
                "pain_focus": "Đừng cố đọc sách hay tập thể dục, hãy trở thành kiểu người ham đọc sách và yêu thể thao. Thay đổi thói quen phải bắt đầu từ căn tính 'Tôi là ai?'.",
                "hook_seed": "Đừng cố gắng đọc sách hay tập thể dục nữa... Trừ khi bạn thay đổi CĂN TÍNH của chính mình!",
                "cliffhanger": "Hãy xem lại từ Tập 1 để xây dựng lại hệ thống thói quen của bạn, và cuốn sách gối đầu giường này đang có ở bình luận ghim.",
                "scenes": [
                    {"query": "person looking sharply and calmly in mirror morning light", "duration": 6.5},
                    {"query": "artist painting bold brushstroke on canvas studio focus", "duration": 6.0},
                    {"query": "runner crossing morning city bridge silhouette dawn", "duration": 6.5},
                    {"query": "writing in leather journal with fountain pen steady hand", "duration": 6.0},
                    {"query": "satisfied smile closing heavy book at sunset window", "duration": 6.0},
                    {"query": "confident steady footsteps walking forward clean marble", "duration": 6.0},
                    {"query": "standing strong in open field facing morning breeze", "duration": 6.5},
                    {"query": "taking a deep breath of fresh mountain air peaceful", "duration": 6.0},
                    {"query": "looking out at glowing city sunrise from high floor", "duration": 6.5},
                    {"query": "silhouette walking boldly into bright golden light path", "duration": 6.5}
                ]
            }

        ]
    }

]

