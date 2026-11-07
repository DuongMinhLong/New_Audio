#!/usr/bin/env python3
"""
multi_series_batch2_metadata.py - Metadata and scene queries for Multi-Part Series Batch 2
Next 3 classic titles x 4 episodes = 12 episodes total:
  1. Đắc Nhân Tâm (Dale Carnegie)
  2. Deep Work (Cal Newport)
  3. Can't Hurt Me (David Goggins)
"""

BATCH_2_SERIES = [
    {
        "series_slug": "dac_nhan_tam",
        "book_title": "Đắc Nhân Tâm",
        "author": "Dale Carnegie",
        "category": "Giao Tiếp & Ứng Xử",
        "shopee_aff_link": "https://s.shopee.vn/9fM4fXL52o",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú Tát Thức Tỉnh: Ảo Tưởng 'Khéo Ăn Nói' & Bẫy Thảo Mai",
                "pain_focus": "Cố uốn lưỡi khen ngợi gượng gạo, cười trừ giả tạo; người đối diện ngửi thấy mùi thảo mai, xu nịnh từ xa và khinh thường thầm kín.",
                "hook_seed": "Bạn tưởng mình khéo ăn nói... Thật ra người ta chỉ thấy bạn THẢO MAI và GIẢ TẠO!",
                "cliffhanger": "Nhưng nếu không khen nịnh, làm sao để một người xa lạ ngay lập tức mở lòng và lắng nghe bạn? Bí mật ở Tập 2...",
                "scenes": [
                    {"query": "fake smile awkward handshake business meeting", "duration": 6.0},
                    {"query": "person texting on phone rolling eyes annoyed", "duration": 6.5},
                    {"query": "two people talking in office one looking away bored", "duration": 6.0},
                    {"query": "whisper gossip behind back dark corridor", "duration": 6.0},
                    {"query": "person drinking alone in noisy crowded bar", "duration": 6.5},
                    {"query": "mirror reflection removing fake smile exhausted face", "duration": 6.0},
                    {"query": "honest calm eye contact across coffee table", "duration": 6.0},
                    {"query": "sincere nod listening intently to partner", "duration": 6.5},
                    {"query": "walking away from superficial cocktail party", "duration": 6.0},
                    {"query": "quiet contemplative silhouette under night street lamp", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh Giới Thực Chiến: Nghệ Thuật Lắng Nghe & Đặt Cái Tôi Xuống Đất",
                "pain_focus": "Cướp lời người khác, chỉ chực chờ họ dứt câu để khoe về bản thân; bí quyết lớn nhất của Carnegie là biến người khác thành nhân vật chính.",
                "hook_seed": "Lý do người ta lảng tránh nói chuyện với bạn... là vì cái mồm bạn không chịu ngừng KHOE VỀ MÌNH!",
                "cliffhanger": "Nhưng khi đối phương sai rành rành và xúc phạm bạn, làm thế nào để xử lý mà không biến thành kẻ thua cuộc? Bí mật ở Tập 3...",
                "scenes": [
                    {"query": "person talking animatedly while other checks watch", "duration": 6.0},
                    {"query": "hand gesturing stop closing mouth shut firmly", "duration": 6.0},
                    {"query": "nodding slowly listening deeply coffee shop", "duration": 6.5},
                    {"query": "person leaning forward showing genuine interest", "duration": 6.0},
                    {"query": "notepad pen writing down key insights listening", "duration": 6.0},
                    {"query": "warm comforting hand on shoulder understanding", "duration": 6.5},
                    {"query": "gentle smile of mutual respect meeting room", "duration": 6.0},
                    {"query": "walking together side by side discussing peacefully", "duration": 6.5},
                    {"query": "two friends sharing deep honest conversation park", "duration": 6.0},
                    {"query": "golden sunset reflection on calm quiet water", "duration": 6.5}
                ]
            }
            ,
            {
                "episode": 3,
                "sub_angle": "Bóc Trần Mặt Tối: Nghịch Lý Tranh Cãi & Thất Bại Của Kẻ Luôn Đúng",
                "pain_focus": "Cố cãi thắng đồng nghiệp, người yêu hay sếp trong mọi cuộc tranh luận; bạn thắng lý lẽ nhưng mất đi mối quan hệ mãi mãi.",
                "hook_seed": "Mỗi lần bạn cãi thắng người ta một vế... Bạn vừa tự tay CHẶT ĐỨT một mối quan hệ!",
                "cliffhanger": "Vậy cảnh giới tối cao của Đắc Nhân Tâm là gì, khi bạn không cần phải cố làm hài lòng bất kỳ ai? Câu trả lời ở Tập 4...",
                "scenes": [
                    {"query": "angry finger pointing argument meeting table", "duration": 6.0},
                    {"query": "red face person shouting in silent frustration", "duration": 6.5},
                    {"query": "broken glass vase on floor shattered pieces", "duration": 6.0},
                    {"query": "cold silent standoff two people looking away", "duration": 6.5},
                    {"query": "person sitting alone with regret head in hands", "duration": 6.0},
                    {"query": "deep breath stepping back releasing anger", "duration": 6.0},
                    {"query": "calm steady handshake resolving dispute", "duration": 6.5},
                    {"query": "warm tea poured into cup peaceful resolution", "duration": 6.0},
                    {"query": "walking away from pointless street argument", "duration": 6.0},
                    {"query": "solitary mountain peak calm above turbulent clouds", "duration": 6.5}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn Bẩy Căn Tính: Đắc Nhân Tâm Đích Thực & Bản Lĩnh Sống Tử Tế",
                "pain_focus": "Đắc Nhân Tâm không phải là kỹ xảo thao túng; nó là bản lĩnh tự tin vào giá trị bản thân, tôn trọng nhân phẩm con người và không sợ bị ghét.",
                "hook_seed": "Đỉnh cao của Đắc Nhân Tâm... là bạn KHÔNG CẦN cố gắng làm hài lòng bất kỳ ai!",
                "cliffhanger": "Hãy xem lại từ Tập 1 để nắm trọn vẹn nghệ thuật này, và cuốn sách kinh điển gối đầu giường đang nằm ở bình luận ghim.",
                "scenes": [
                    {"query": "confident person walking tall through city lobby", "duration": 6.5},
                    {"query": "genuine warm smile looking straight into camera", "duration": 6.0},
                    {"query": "helping colleague pick up dropped files kindness", "duration": 6.0},
                    {"query": "firm trustworthy handshake closing deal", "duration": 6.5},
                    {"query": "standing calm in busy crowded subway train", "duration": 6.0},
                    {"query": "open hands holding warm glowing light concept", "duration": 6.0},
                    {"query": "looking at vast ocean horizon peaceful composure", "duration": 6.5},
                    {"query": "turning page of classic book in library quiet", "duration": 6.0},
                    {"query": "sunrise illuminating modern architectural facade", "duration": 6.5},
                    {"query": "silhouette walking forward into golden morning light", "duration": 6.5}
                ]
            }

        ]
    }
    ,
    {
        "series_slug": "deep_work",
        "book_title": "Deep Work (Làm Việc Sâu)",
        "author": "Cal Newport",
        "category": "Năng Suất & Kỹ Năng Làm Việc",
        "shopee_aff_link": "https://s.shopee.vn/5q9M6UZfpD",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú Tát Thức Tỉnh: Ảo Tưởng 'Bận Rộn' & Hội Chứng Não Mục Rỗng",
                "pain_focus": "Lướt short video liên tục làm giảm dopamine threshold, não sương mù, mở 20 tab trình duyệt nhưng 4 tiếng không xong 1 trang tài liệu; giả vờ bận rộn để trốn việc khó.",
                "hook_seed": "Bạn không hề bận rộn... Bạn chỉ đang GIẢ VỜ BẬN để trốn tránh việc khó!",
                "cliffhanger": "Nhưng làm sao để não bộ cai nghiện dopamine rẻ tiền và bước vào trạng thái làm việc sâu? Chiến thuật ở Tập 2...",
                "scenes": [
                    {"query": "finger scrolling endlessly on smartphone screen fast", "duration": 6.0},
                    {"query": "person staring dazed with red eyes at computer screen", "duration": 6.5},
                    {"query": "chaotic messy browser with dozens of open tabs", "duration": 6.0},
                    {"query": "clock hands spinning wildly fast time passing", "duration": 6.0},
                    {"query": "hands shaking reaching for phone notification ping", "duration": 6.5},
                    {"query": "throwing phone face down on wooden desk firmly", "duration": 6.0},
                    {"query": "deep breath closing eyes rubbing temples", "duration": 6.0},
                    {"query": "single glowing monitor in pitch dark quiet room", "duration": 6.5},
                    {"query": "person staring out rainy window contemplating", "duration": 6.0},
                    {"query": "lone tree standing still in foggy morning meadow", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh Giới Thực Chiến: Khung Giờ Bất Khả Xâm Phạm & Nghi Thức 90 Phút",
                "pain_focus": "Bật chế độ máy bay, đóng cửa phòng, chia khối thời gian 90 phút Deep Work buổi sáng khi não chưa bị ô nhiễm bởi tin tức xã hội.",
                "hook_seed": "Nếu bạn không dám tắt thông báo trong chín mươi phút... Đời bạn đã bị kẻ khác ĐOẠT MẤT!",
                "cliffhanger": "Nhưng bạn có biết lý do sâu xa vì sao 90% người cố làm việc sâu vẫn thất bại thảm hại? Lỗ hổng ở Tập 3...",
                "scenes": [
                    {"query": "turning phone to silent airplane mode setting face down", "duration": 6.0},
                    {"query": "closing office door firmly hanging do not disturb sign", "duration": 6.5},
                    {"query": "setting mechanical timer 90 minutes ticking", "duration": 6.0},
                    {"query": "noise cancelling headphones put on ears focus", "duration": 6.5},
                    {"query": "fingers typing rapidly and steadily on keyboard", "duration": 6.0},
                    {"query": "steam rising from fresh black coffee cup beside laptop", "duration": 6.0},
                    {"query": "pen writing clean structured outline on notebook", "duration": 6.5},
                    {"query": "clock ticking quietly steady deep work rhythm", "duration": 6.0},
                    {"query": "turning page of research paper deep concentration", "duration": 6.5},
                    {"query": "calm smile of deep accomplishment looking up", "duration": 6.0}
                ]
            }
            ,
            {
                "episode": 3,
                "sub_angle": "Bóc Trần Mặt Tối: Cái Bẫy 'Đa Nhiệm' & Nỗi Sợ Bị AI Đào Thải",
                "pain_focus": "Vừa làm vừa check tin nhắn Slack/Zalo làm IQ giảm tương đương thức trắng đêm; những công việc hời hợt (Shallow Work) sẽ bị AI thay thế 100% trong 2 năm tới.",
                "hook_seed": "Làm nhiều việc cùng lúc không phải là tài năng... Đó là cách nhanh nhất biến bạn thành KẺ TẦM THƯỜNG!",
                "cliffhanger": "Khi AI làm việc hời hợt nhanh hơn bạn gấp ngàn lần, vũ khí duy nhất để bạn không bao giờ bị đào thải là gì? Khám phá ở Tập 4...",
                "scenes": [
                    {"query": "person switching rapidly between messaging apps laptop", "duration": 6.0},
                    {"query": "robotic arm typing on computer futuristic code", "duration": 6.5},
                    {"query": "brain scan graphic flickering chaotic stress signals", "duration": 6.0},
                    {"query": "person holding head in hands overwhelmed by notifications", "duration": 6.5},
                    {"query": "paper shredder destroying superficial documents", "duration": 6.0},
                    {"query": "stepping away from screen walking to window calm", "duration": 6.0},
                    {"query": "focused artisan polishing gemstone macro precision", "duration": 6.5},
                    {"query": "complex mathematical equations written on blackboard", "duration": 6.0},
                    {"query": "calm face of master craftsperson in workshop", "duration": 6.5},
                    {"query": "glowing blue light fiber optic network concept", "duration": 6.0}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn Bẩy Đột Phá: Siêu Năng Lực Thời Đại Số & Bản Lĩnh Tạo Giá Trị Hiếm",
                "pain_focus": "Khả năng tập trung sâu 4 tiếng/ngày là siêu năng lực hiếm hoi của thế kỷ 21; ai làm chủ được nó sẽ làm chủ thị trường và kiếm gấp 10 lần người khác.",
                "hook_seed": "Khả năng ngồi yên một chỗ và tập trung sâu... là SIÊU NĂNG LỰC DUY NHẤT cứu bạn khỏi bị đào thải!",
                "cliffhanger": "Hãy xem lại từ Tập 1 để rèn luyện lại bộ não của bạn, và cuốn sách gối đầu giường này đang có ở bình luận ghim.",
                "scenes": [
                    {"query": "person working deeply in grand quiet library sunlight", "duration": 6.5},
                    {"query": "architect sketching master blueprint architectural desk", "duration": 6.0},
                    {"query": "master musician playing cello eyes closed flow state", "duration": 6.5},
                    {"query": "programmer solving complex code breakthrough moment", "duration": 6.0},
                    {"query": "looking at completed masterpiece product satisfaction", "duration": 6.0},
                    {"query": "closing laptop with absolute confidence end of day", "duration": 6.5},
                    {"query": "walking peacefully outdoors in sunlit autumn forest", "duration": 6.0},
                    {"query": "breathing deeply on mountain overlook feeling free", "duration": 6.5},
                    {"query": "golden sunrise piercing through modern glass towers", "duration": 6.0},
                    {"query": "silhouette standing steady against fast rushing world", "duration": 6.5}
                ]
            }

        ]
    }
    ,
    {
        "series_slug": "cant_hurt_me",
        "book_title": "Can't Hurt Me (Không Thể Làm Tôi Tổn Thương)",
        "author": "David Goggins",
        "category": "Ý Chí & Kỷ Luật Thép",
        "shopee_aff_link": "https://s.shopee.vn/AKblSlIXh0",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú Tát Thức Tỉnh: Cái Bẫy 'Chữa Lành' & Hội Chứng Nằm Ườn",
                "pain_focus": "Hơi áp lực là xin nghỉ việc 'để chữa lành'; nằm ườn trên giường ôm điện thoại than thở trầm cảm; lấy cớ tổn thương để trốn tránh trách nhiệm trưởng thành.",
                "hook_seed": "Hơi áp lực một chút là xin nghỉ 'để chữa lành'... Sự thật là: Bạn không tổn thương... Bạn chỉ đang HÈN NHÁT!",
                "cliffhanger": "Nhưng khi bạn thấy mình chạm đáy và muốn bỏ cuộc, bí mật nào của lính đặc nhiệm sẽ cứu bạn dậy? Sự thật ở Tập 2...",
                "scenes": [
                    {"query": "person lying in dark messy bed staring at glowing phone", "duration": 6.0},
                    {"query": "messy bedroom clothes scattered pizza box floor", "duration": 6.0},
                    {"query": "alarm clock ringing 11am person pulling blanket over head", "duration": 6.5},
                    {"query": "heavy tired sigh staring into dark empty room", "duration": 6.0},
                    {"query": "splashing cold water forcefully onto face bathroom", "duration": 6.5},
                    {"query": "harsh fluorescent light reflecting intense eyes in mirror", "duration": 6.0},
                    {"query": "tying running shoe laces tightly on cold concrete", "duration": 6.5},
                    {"query": "pushing open heavy steel door stepping into freezing rain", "duration": 6.0},
                    {"query": "running alone in dark empty street early 4am", "duration": 6.5},
                    {"query": "silhouette of determined runner under lone street lamp", "duration": 6.0}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh Giới Thực Chiến: Quy Tắc 40% Của Navy SEAL",
                "pain_focus": "Khi não gào thét bảo bạn phải dừng lại vì kiệt sức, bạn thực chất mới chỉ chạm đến 40% giới hạn thực của cơ thể; não sinh ra để bảo vệ bạn khỏi nguy hiểm chứ không muốn bạn thành công.",
                "hook_seed": "Mỗi khi não bạn gào lên 'mệt quá rồi'... Bạn thực ra mới chỉ dùng BỐN MƯƠI PHẦN TRĂM công lực!",
                "cliffhanger": "Nhưng làm sao để vượt qua sự lười biếng ăn sâu vào tiềm thức mỗi buổi sáng? Vũ khí tàn nhẫn ở Tập 3...",
                "scenes": [
                    {"query": "runner gasping heavily for breath sweat dripping chin", "duration": 6.5},
                    {"query": "athlete clenching fists looking down at asphalt pain", "duration": 6.0},
                    {"query": "internal struggle eye closeup intense grit determination", "duration": 6.5},
                    {"query": "breaking through physical exhaustion barrier running faster", "duration": 6.0},
                    {"query": "doing pullups on metal bar muscle strain veins", "duration": 6.5},
                    {"query": "dripping wet Navy SEAL training in freezing ocean waves", "duration": 6.0},
                    {"query": "screaming inside pushing past the mental barrier", "duration": 6.0},
                    {"query": "steady powerful breath recovering composure", "duration": 6.5},
                    {"query": "standing upright shoulders back refusing to sit down", "duration": 6.0},
                    {"query": "sunrise breaking over running track empty stadium", "duration": 6.5}
                ]
            }
            ,
            {
                "episode": 3,
                "sub_angle": "Bóc Trần Mặt Tối: Chiếc Gương Trách Nhiệm (Accountability Mirror)",
                "pain_focus": "Đứng trước gương và lột trần toàn bộ sự dối trá của mình: 'Mày đang béo, mày đang lười, mày đang nghèo vì mày hèn'; dán giấy ghi chú lỗi sai lên gương và giải quyết từng cái một.",
                "hook_seed": "Hãy đứng trước gương và nói thẳng vào mặt mình: Mày đang nghèo và béo... vì MÀY HÈN!",
                "cliffhanger": "Khi bạn đã dám đối diện với sự thật nhục nhã nhất, làm sao để biến nó thành ngọn lửa thiêu đốt đối thủ? Tuyệt chiêu ở Tập 4...",
                "scenes": [
                    {"query": "person standing close in front of steamy bathroom mirror", "duration": 6.5},
                    {"query": "wiping fog off mirror revealing sharp critical gaze", "duration": 6.0},
                    {"query": "yellow sticky notes pasted on mirror with harsh truths", "duration": 6.5},
                    {"query": "ripping off sticky note after completing hard task", "duration": 6.0},
                    {"query": "clenched jaw looking directly into own reflection", "duration": 6.0},
                    {"query": "writing down brutally honest weaknesses in notebook", "duration": 6.5},
                    {"query": "deep breath acknowledging mistakes standing tall", "duration": 6.0},
                    {"query": "running up steep concrete stairs determined pace", "duration": 6.5},
                    {"query": "lifting heavy weights chalk dust floating in gym light", "duration": 6.0},
                    {"query": "standing outside in pouring rain looking up fearless", "duration": 6.5}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn Bẩy Căn Tính: Lấy Linh Hồn Của Nghịch Cảnh (Taking Souls)",
                "pain_focus": "Biến sự sỉ nhục, coi thường của người khác và nỗi đau thể xác thành năng lượng đẩy bạn tiến lên; không có hoàn cảnh nào bẻ gãy được bạn nếu tâm trí bạn đã trơ lì.",
                "hook_seed": "Kẻ thù lớn nhất không phải người đời chê bai... Kẻ thù là tiếng nói hèn nhát TRONG ĐẦU BẠN!",
                "cliffhanger": "Hãy xem lại từ Tập 1 để cài đặt lại ý chí thép của bạn, và cuốn sách làm rung chuyển hàng triệu người này đang có ở bình luận ghim.",
                "scenes": [
                    {"query": "standing on rocky mountain ridge howling wind fearless", "duration": 6.5},
                    {"query": "intense focused stare of warrior after brutal battle", "duration": 6.0},
                    {"query": "running through torrential rainstorm storm thunder", "duration": 6.5},
                    {"query": "smiling calmly in middle of extreme adversity grit", "duration": 6.0},
                    {"query": "lifting heavy kettlebell sweat falling slow motion", "duration": 6.5},
                    {"query": "looking down at city lights from high mountain summit", "duration": 6.0},
                    {"query": "placing hand over heart steady controlled breathing", "duration": 6.0},
                    {"query": "walking forward through thick fog into golden sunlight", "duration": 6.5},
                    {"query": "iron chain breaking into pieces high tension concept", "duration": 6.0},
                    {"query": "silhouette of lone champion standing tall on summit sunset", "duration": 6.5}
                ]
            }

        ]
    }


]
