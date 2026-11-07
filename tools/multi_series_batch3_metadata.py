#!/usr/bin/env python3
"""
multi_series_batch3_metadata.py - Metadata and scene queries for Multi-Part Series Batch 3 (Gói 1)
4 classic titles x 4 episodes = 16 episodes total:
  1. Đi Tìm Lẽ Sống (Viktor Frankl)
  2. Nghệ Thuật Sống (Seneca)
  3. Kỷ Luật Là Tự Do (Jocko Willink)
  4. Tư Duy Nhanh Và Chậm (Daniel Kahneman)
"""

BATCH_3_SERIES = [
    {
        "series_slug": "di_tim_le_song",
        "book_title": "Đi Tìm Lẽ Sống",
        "author": "Viktor Frankl",
        "category": "Triết Lý & Ý Nghĩa Sống",
        "shopee_aff_link": "https://s.shopee.vn/AUvBf4HuM3",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú tát thức tỉnh: Cái bẫy theo đuổi hạnh phúc và hội chứng trống rỗng",
                "pain_focus": "Càng đuổi theo niềm vui và sự thoải mái ngắn hạn thì càng thấy cô đơn, vô nghĩa; hạnh phúc không thể tìm kiếm trực tiếp mà chỉ là kết quả phụ của việc sống có mục đích.",
                "hook_seed": "Lý do bạn càng cố tìm kiếm hạnh phúc thì càng rơi vào trầm cảm và trống rỗng.",
                "cliffhanger": "Nhưng khi nghịch cảnh ập đến và tước đoạt mọi thứ, làm sao để tìm ra ý nghĩa trong nỗi đau? Lời giải ở tập 2.",
                "scenes": [
                    {"query": "lonely person sitting in luxury apartment city night lights", "duration": 6.5},
                    {"query": "tired face looking in bathroom mirror exhaustion neon", "duration": 6.0},
                    {"query": "walking alone in foggy quiet autumn street dusk", "duration": 6.5},
                    {"query": "clock ticking in empty dark living room lonely", "duration": 6.0},
                    {"query": "silhouette looking through window raindrops pouring", "duration": 6.5},
                    {"query": "taking off heavy winter coat sighing sitting alone", "duration": 6.0},
                    {"query": "hand touching cold glass window looking outside", "duration": 6.0},
                    {"query": "deep thoughtful breath facing city skyline dusk", "duration": 6.5},
                    {"query": "turning page of old classic book warm lamp", "duration": 6.0},
                    {"query": "single candle flame burning steady in darkness", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh giới thực chiến: Quyền tự do cuối cùng của con người",
                "pain_focus": "Người ta có thể lấy đi tiền tài, sức khỏe, địa vị của bạn, nhưng không ai có thể tước đoạt quyền lựa chọn thái độ sống của bạn trước nghịch cảnh.",
                "hook_seed": "Thiên hạ có thể cướp sạch mọi thứ của bạn, ngoại trừ một thứ duy nhất.",
                "cliffhanger": "Nhưng bạn có biết vì sao phần lớn người ta vẫn cam chịu làm nô lệ cho hoàn cảnh? Bí mật ở tập 3.",
                "scenes": [
                    {"query": "barbed wire fence in mist cold winter atmosphere", "duration": 6.0},
                    {"query": "person standing firm against strong howling wind", "duration": 6.5},
                    {"query": "intense calm eye closeup direct look determination", "duration": 6.0},
                    {"query": "stepping forward across muddy cold ground boots", "duration": 6.5},
                    {"query": "breaking free from heavy iron chain macro slow", "duration": 6.0},
                    {"query": "taking a slow deep breath looking into storm", "duration": 6.5},
                    {"query": "warm sunlight beam piercing through thick storm clouds", "duration": 6.0},
                    {"query": "man standing proud on rocky shore facing ocean waves", "duration": 6.5},
                    {"query": "holding small piece of bread with gratitude quiet", "duration": 6.0},
                    {"query": "silhouette walking toward rising sun mountain horizon", "duration": 6.5}
                ]
            },
            {
                "episode": 3,
                "sub_angle": "Bóc trần mặt tối: Căn bệnh than thở và vai diễn nạn nhân",
                "pain_focus": "Lấy cớ số phận hẩm hiu để trốn tránh trách nhiệm với cuộc đời; thay vì hỏi đời sẽ cho ta điều gì, hãy tự hỏi cuộc đời đang đòi hỏi điều gì ở bạn.",
                "hook_seed": "Đừng hỏi cuộc đời này nợ bạn những gì, hãy hỏi bạn đã làm được gì cho đời.",
                "cliffhanger": "Khi dẹp bỏ tâm lý nạn nhân, điểm tựa tối thượng nào giúp bạn đứng vững giữa bão tố? Khám phá ở tập 4.",
                "scenes": [
                    {"query": "person sitting on floor with head buried in knees", "duration": 6.0},
                    {"query": "shattered ceramic cup on floor dramatic shadows", "duration": 6.5},
                    {"query": "looking at reflection in cracked broken mirror", "duration": 6.0},
                    {"query": "rain hitting muddy ground outside window darkness", "duration": 6.5},
                    {"query": "splashing cold face water looking up with resolve", "duration": 6.0},
                    {"query": "standing up straight dusting off clothes determined", "duration": 6.5},
                    {"query": "opening heavy metal door stepping into sunlight", "duration": 6.0},
                    {"query": "hands helping someone stand up from ground kindness", "duration": 6.5},
                    {"query": "calm steady smile looking straight into camera", "duration": 6.0},
                    {"query": "walking forward with purposeful stride clean street", "duration": 6.5}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn bẩy giải phóng: Ai có một lý do để sống sẽ chịu được mọi nghịch cảnh",
                "pain_focus": "Nietzsche từng nói: Người có lý do để sống có thể vượt qua hầu như mọi nghịch cảnh. Tìm ra lý tưởng phụng sự là chìa khóa mở cánh cửa tự do nội tâm.",
                "hook_seed": "Chỉ cần trong tim bạn có một lý do để sống, không nghịch cảnh nào đánh gục được bạn.",
                "cliffhanger": "Hãy xem lại từ tập 1 để thấu hiểu trọn vẹn triết lý này, cuốn sách kinh điển gối đầu giường đang nằm ở bình luận ghim.",
                "scenes": [
                    {"query": "lone climber reaching mountain summit sunrise golden", "duration": 6.5},
                    {"query": "deep chest breath standing tall in fresh mountain air", "duration": 6.0},
                    {"query": "open hands letting wind blow through fingers peaceful", "duration": 6.5},
                    {"query": "warm sunlight illuminating genuine serene smile", "duration": 6.0},
                    {"query": "closing heavy classic leather book with quiet joy", "duration": 6.0},
                    {"query": "walking peacefully through quiet blooming spring garden", "duration": 6.5},
                    {"query": "standing fearless on high cliff overlooking vast valley", "duration": 6.5},
                    {"query": "watching bright sunrise horizon reflection ocean", "duration": 6.0},
                    {"query": "confident steady footsteps forward along marble path", "duration": 6.0},
                    {"query": "silhouette walking into bright warm golden dawn", "duration": 6.5}
                ]
            }
        ]
    },
    {
        "series_slug": "seneca_nghe_thuat_song",
        "book_title": "Nghệ Thuật Sống (Letters from a Stoic)",
        "author": "Seneca",
        "category": "Triết Học Khắc Kỷ & Bản Lĩnh",
        "shopee_aff_link": "https://s.shopee.vn/5LD5VZbZq4",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú tát thức tỉnh: Nỗi sợ tưởng tượng và cái chết trước khi lâm chung",
                "pain_focus": "Seneca chỉ ra: Chúng ta đau khổ trong trí tưởng tượng nhiều hơn là trong thực tế. Đêm nằm lo âu ngày mai phá sản, mất việc, bị chê bai; tự hủy hoại bản thân bằng nỗi sợ hão huyền.",
                "hook_seed": "Điều tàn nhẫn nhất là bạn đau khổ vì những thứ chưa từng xảy ra nhiều hơn là trong đời thực.",
                "cliffhanger": "Nhưng làm sao để não bộ dừng việc tự vẽ ra thảm họa mỗi đêm? Chiến thuật Khắc Kỷ ở tập 2.",
                "scenes": [
                    {"query": "person awake in bed tossing turning 3am ceiling stare", "duration": 6.5},
                    {"query": "anxious hands tapping rhythmically on wooden desk", "duration": 6.0},
                    {"query": "shadows stretching on dark empty bedroom wall", "duration": 6.0},
                    {"query": "splashing cold water on face looking deeply mirror", "duration": 6.5},
                    {"query": "heavy storm blowing trees outside bedroom window", "duration": 6.0},
                    {"query": "hand firmly closing open notebook calm resolve", "duration": 6.0},
                    {"query": "sitting upright taking slow deep diaphragmatic breath", "duration": 6.5},
                    {"query": "looking out at quiet city dawn from high window", "duration": 6.0},
                    {"query": "ancient marble statue stoic face dramatic shadow", "duration": 6.5},
                    {"query": "solitary figure standing calm in foggy morning park", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh giới thực chiến: Bài tập chuẩn bị cho điều tồi tệ nhất",
                "pain_focus": "Kỹ thuật Praemeditatio Malorum của Stoic: Mỗi sáng hãy hình dung mất hết tiền, bị phản bội, đau đớn; khi đã tập dượt với cái tệ nhất, không biến cố nào làm bạn hoảng loạn được.",
                "hook_seed": "Cách duy nhất để bạn không bao giờ suy sụp là hãy tập sống với điều tồi tệ nhất ngay từ sáng nay.",
                "cliffhanger": "Nhưng ranh giới giữa việc chuẩn bị cho cái xấu và tự biến mình thành kẻ bi quan tiêu cực là gì? Sự thật ở tập 3.",
                "scenes": [
                    {"query": "sitting alone in empty minimalist room on wooden floor", "duration": 6.5},
                    {"query": "drinking plain water eating simple crust bread calm", "duration": 6.0},
                    {"query": "ancient roman pillar standing unbroken amid ruins", "duration": 6.5},
                    {"query": "firm calm eye contact directly into camera stoic", "duration": 6.0},
                    {"query": "lightning striking in distance dark stormy sky", "duration": 6.0},
                    {"query": "unflinching face looking directly at storm horizon", "duration": 6.5},
                    {"query": "writing stoic reflections in leather bound diary", "duration": 6.0},
                    {"query": "walking calmly through crowded bustling modern market", "duration": 6.5},
                    {"query": "steady heartbeat calm breathing peaceful posture", "duration": 6.0},
                    {"query": "granite rock standing firm against pounding sea surf", "duration": 6.5}
                ]
            }
            ,
            {
                "episode": 3,
                "sub_angle": "Bóc trần mặt tối: Cơn giận dữ và cái bẫy tự thiêu chính mình",
                "pain_focus": "Seneca viết tác phẩm kinh điển 'Về Cơn Giận' (On Anger): Giận dữ là một dạng điên cuồng ngắn hạn; không có lỗi lầm nào của người khác đáng để ta tự đầu độc tâm trí của chính mình.",
                "hook_seed": "Mỗi khi bạn nổi điên vì người khác, bạn đang uống thuốc độc rồi mong người ta chết.",
                "cliffhanger": "Khi làm chủ được cơn giận, cảnh giới tĩnh lặng cao nhất của một triết gia Khắc Kỷ là gì? Đón xem tập 4.",
                "scenes": [
                    {"query": "clenched fist trembling with anger dramatic red light", "duration": 6.0},
                    {"query": "person taking deep slow breath releasing clenched jaw", "duration": 6.5},
                    {"query": "drops of water falling into calm crystal clear bowl", "duration": 6.0},
                    {"query": "walking away calmly from screaming loud argument", "duration": 6.5},
                    {"query": "looking into deep placid pool of water stillness", "duration": 6.0},
                    {"query": "ancient olive tree rooted firm through centuries", "duration": 6.5},
                    {"query": "pouring warm herbal tea with slow steady hand", "duration": 6.0},
                    {"query": "sitting still in quiet monastery courtyard sunlight", "duration": 6.5},
                    {"query": "calm composed face observing turbulent world softly", "duration": 6.0},
                    {"query": "mountain peak towering majestic in clear blue sky", "duration": 6.5}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn bẩy giải phóng: Về sự ngắn ngủi của đời người và cái chết cận kề",
                "pain_focus": "Cuộc đời không hề ngắn, chỉ là chúng ta lãng phí quá nhiều; Memento Mori: Hãy nhớ rằng bạn sẽ chết, mỗi ngày trôi qua là một phần đời đã vĩnh viễn thuộc về thần chết.",
                "hook_seed": "Bạn không hề thiếu thời gian, bạn chỉ đang ném từng ngày của đời mình vào sọt rác.",
                "cliffhanger": "Hãy xem lại từ tập 1 để rèn luyện bản lĩnh Khắc Kỷ, và cuốn cẩm nang thông thái này đang có ở bình luận ghim.",
                "scenes": [
                    {"query": "sand flowing through antique hourglass macro golden", "duration": 6.5},
                    {"query": "looking at hands aging light shadows sunset", "duration": 6.0},
                    {"query": "closing eyes feeling warm evening breeze on face", "duration": 6.0},
                    {"query": "standing solitary on ocean shore at golden dusk", "duration": 6.5},
                    {"query": "writing final words on vintage parchment pen", "duration": 6.0},
                    {"query": "calm genuine smile of man who has lived fully", "duration": 6.5},
                    {"query": "turning off brass desk lamp peaceful dark room", "duration": 6.0},
                    {"query": "walking forward into misty peaceful dawn forest", "duration": 6.5},
                    {"query": "ancient roman temple ruins bathed in warm twilight", "duration": 6.0},
                    {"query": "silhouette standing serene facing infinite night stars", "duration": 6.5}
                ]
            }

        ]
    }
    ,
    {
        "series_slug": "ky_luat_la_tu_do",
        "book_title": "Kỷ Luật Là Tự Do (Discipline Equals Freedom)",
        "author": "Jocko Willink",
        "category": "Kỷ Luật Thép & Ý Chí",
        "shopee_aff_link": "https://s.shopee.vn/5VWVhsawV7",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú tát thức tỉnh: Cái bẫy tự do buông thả và hội chứng nô lệ của cảm xúc",
                "pain_focus": "Bạn tưởng thích gì làm nấy, ngủ nướng, ăn vặt, lướt điện thoại là tự do; thực chất bạn đang làm nô lệ cho từng cơn nghiện dopamine rẻ tiền và sự lười biếng.",
                "hook_seed": "Thích gì làm nấy không phải là tự do, đó là sự nô lệ nhục nhã nhất của một con người.",
                "cliffhanger": "Nhưng làm sao để thức dậy lúc bốn giờ ba mươi sáng và đè bẹp tiếng nói lười biếng trong đầu? Chiến thuật đặc nhiệm ở tập 2.",
                "scenes": [
                    {"query": "person sleeping in messy room morning light phone glowing", "duration": 6.0},
                    {"query": "alarm clock ringing 430am hand snapping it off immediately", "duration": 6.5},
                    {"query": "feet hitting cold wooden floor firmly without hesitation", "duration": 6.0},
                    {"query": "splashing ice cold water on face in dark bathroom", "duration": 6.5},
                    {"query": "tying combat training boots tightly dim morning light", "duration": 6.0},
                    {"query": "steely intense gaze of determined athlete in mirror", "duration": 6.0},
                    {"query": "stepping outside into pitch black freezing morning air", "duration": 6.5},
                    {"query": "running rhythmically on empty dawn road lone breath", "duration": 6.5},
                    {"query": "barbell loaded with iron weights dim garage gym", "duration": 6.0},
                    {"query": "silhouette lifting heavy barbell overhead sunrise breaking", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh giới thực chiến: Đừng đàm phán với điểm yếu của bản thân",
                "pain_focus": "Quy tắc thép của lính đặc nhiệm: Tuyệt đối không bao giờ thương lượng với sự lười biếng; khi đồng hồ reo, không đắn đo, không suy nghĩ, lập tức bật dậy và hành động.",
                "hook_seed": "Giây phút bạn bắt đầu suy nghĩ xem có nên dậy hay không, bạn đã thua rồi.",
                "cliffhanger": "Nhưng khi bạn thấy mình kiệt sức và cảm xúc tuột dốc, bí quyết kiểm soát tâm trí của Jocko là gì? Đón xem tập 3.",
                "scenes": [
                    {"query": "heavy rain pouring outside running track empty", "duration": 6.0},
                    {"query": "athlete doing burpees in cold mud dripping sweat", "duration": 6.5},
                    {"query": "intense jaw clenching pushing past burning muscle pain", "duration": 6.0},
                    {"query": "kettlebell swinging rhythmically powerful hips", "duration": 6.5},
                    {"query": "sweat dripping from chin onto cold concrete floor", "duration": 6.0},
                    {"query": "chalk dust floating in air hands gripping pullup bar", "duration": 6.5},
                    {"query": "clock ticking precisely steady rhythmic progression", "duration": 6.0},
                    {"query": "deep controlled rhythmic breathing warrior pose", "duration": 6.5},
                    {"query": "standing upright refused to lean against wall strength", "duration": 6.0},
                    {"query": "first golden light of sun breaking over dark hills", "duration": 6.5}
                ]
            }
            ,
            {
                "episode": 3,
                "sub_angle": "Bóc trần mặt tối: Triết lý 'Tốt thôi' (Good) trước mọi thảm họa",
                "pain_focus": "Dự án đổ bể? Tốt thôi, ta có cơ hội làm lại thông minh hơn. Bị sa thải? Tốt thôi, ta có thời gian nâng cấp bản thân. Thất bại là bài học tôi luyện ý chí.",
                "hook_seed": "Mỗi khi biến cố tồi tệ nhất ập đến, câu đầu tiên bạn nên nói là: Tốt thôi.",
                "cliffhanger": "Khi đã biến mọi thất bại thành vũ khí, cảnh giới tự do tuyệt đối mà kỷ luật mang lại là gì? Khám phá ở tập 4.",
                "scenes": [
                    {"query": "computer screen showing system error red warning text", "duration": 6.0},
                    {"query": "person taking deep calm breath instead of panicking", "duration": 6.5},
                    {"query": "smiling quietly with stoic confidence in adversity", "duration": 6.0},
                    {"query": "opening a clean blank notebook writing new strategy", "duration": 6.5},
                    {"query": "blacksmith hammering glowing iron anvil sparks flying", "duration": 6.0},
                    {"query": "sweat and focus working through late night desk lamp", "duration": 6.5},
                    {"query": "firm steady footsteps marching through cold wind", "duration": 6.0},
                    {"query": "lifting heavy sandbag over shoulder rugged terrain", "duration": 6.5},
                    {"query": "calm composed expression looking straight into camera", "duration": 6.0},
                    {"query": "standing fearless on high summit looking at sunrise", "duration": 6.5}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn bẩy căn tính: Kỷ luật là tự do đích thực",
                "pain_focus": "Kỷ luật tài chính mang lại tự do tiền bạc. Kỷ luật tập luyện mang lại tự do thể xác. Kỷ luật học tập mang lại tự do trí tuệ. Muốn tự do, bạn phải rèn luyện kỷ luật thép.",
                "hook_seed": "Bạn muốn tự do về tiền bạc và thời gian, nhưng bạn lại hèn nhát trước kỷ luật.",
                "cliffhanger": "Hãy xem lại từ tập 1 để xây dựng ý chí thép của bạn, cuốn cẩm nang gối đầu giường này đang có ở bình luận ghim.",
                "scenes": [
                    {"query": "calm runner pacing steadily along misty riverbank dawn", "duration": 6.5},
                    {"query": "focused craftsman carving intricate wood piece workshop", "duration": 6.0},
                    {"query": "person closing laptop cleanly at end of productive day", "duration": 6.0},
                    {"query": "taking a deep breath of fresh ocean air open horizon", "duration": 6.5},
                    {"query": "standing tall on rocky ridge arms wide open freedom", "duration": 6.5},
                    {"query": "closing heavy classic black book with quiet power", "duration": 6.0},
                    {"query": "unshakable gaze looking straight ahead fearless", "duration": 6.0},
                    {"query": "walking forward with unwavering confidence marble hall", "duration": 6.5},
                    {"query": "golden morning sun illuminating modern architectural skyline", "duration": 6.0},
                    {"query": "silhouette walking into bright golden dawn light victory", "duration": 6.5}
                ]
            }

        ]
    }

    ,
    {
        "series_slug": "tu_duy_nhanh_va_cham",
        "book_title": "Tư Duy Nhanh Và Chậm (Thinking, Fast and Slow)",
        "author": "Daniel Kahneman",
        "category": "Tâm Lý Học Nhận Thức & Quyết Định",
        "shopee_aff_link": "https://s.shopee.vn/5fpvuBaJAA",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú tát thức tỉnh: Ảo tưởng lý trí và cái bẫy của Hệ Thống 1",
                "pain_focus": "Bạn luôn nghĩ mình là người hành động logic, nhưng thực chất 95% quyết định mua sắm, yêu đương, cãi vã đều do Hệ Thống 1 bản năng, lười biếng và đầy thiên kiến thao túng.",
                "hook_seed": "Bạn tưởng mình sống bằng lý trí, sự thật là bạn đang để bản năng dắt mũi từng phút.",
                "cliffhanger": "Nhưng làm sao để kích hoạt Hệ Thống 2 tư duy sâu trước khi đưa ra quyết định sai lầm tiền bạc? Khám phá ở tập 2.",
                "scenes": [
                    {"query": "person impulse buying online credit card checkout screen", "duration": 6.0},
                    {"query": "staring at flashing stock ticker chart in anxiety", "duration": 6.5},
                    {"query": "brain animation glowing fast chaotic neural firings", "duration": 6.0},
                    {"query": "person rubbing eyes realizing costly financial mistake", "duration": 6.5},
                    {"query": "hands holding head in hands regret over argument", "duration": 6.0},
                    {"query": "taking a slow pause closing eyes stepping back", "duration": 6.5},
                    {"query": "writing down structured logic tree on paper pen", "duration": 6.0},
                    {"query": "looking closely at fine print contract with magnifying glass", "duration": 6.5},
                    {"query": "calm thoughtful face of analyst at desk night", "duration": 6.0},
                    {"query": "steady pendulum swinging in slow rhythmic motion", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh giới thực chiến: Cái bẫy mỏ neo và nghệ thuật đàm phán",
                "pain_focus": "Hiệu ứng mỏ neo (Anchoring Effect): Con số đầu tiên bạn nghe thấy sẽ vô thức chi phối toàn bộ phán đoán của bạn; kẻ khôn ngoan luôn biết cách gài mỏ neo và phá mỏ neo của đối phương.",
                "hook_seed": "Con số đầu tiên bạn nghe thấy chính là cái bẫy tinh vi nhất khiến bạn mất tiền.",
                "cliffhanger": "Nhưng lý do vì sao người thông minh vẫn dễ dàng sập bẫy các dự án lừa đảo lại nằm ở Tập 3.",
                "scenes": [
                    {"query": "price tag on luxury store item macro numbers focus", "duration": 6.0},
                    {"query": "hand firmly crossing out inflated price on contract", "duration": 6.5},
                    {"query": "two businessmen negotiating across sleek modern table", "duration": 6.0},
                    {"query": "calm confident person looking steadily at opponent", "duration": 6.5},
                    {"query": "calculator display calculating complex percentage", "duration": 6.0},
                    {"query": "deep thoughtful pause before giving final counter offer", "duration": 6.5},
                    {"query": "firm handshake sealing win win business agreement", "duration": 6.0},
                    {"query": "sipping espresso quietly observing bustling room", "duration": 6.5},
                    {"query": "chess player moving wooden knight with strategic precision", "duration": 6.0},
                    {"query": "sunset shining through architectural glass skyscraper office", "duration": 6.5}
                ]
            }
            ,
            {
                "episode": 3,
                "sub_angle": "Bóc trần mặt tối: Nghịch lý sợ mất mát (Loss Aversion)",
                "pain_focus": "Nỗi đau mất 1 triệu đồng lớn gấp đôi niềm vui khi kiếm được 1 triệu; chính tâm lý sợ mất mát khiến bạn gồng lỗ đầu tư, cố chấp níu kéo công việc độc hại hoặc mối quan hệ tồi tàn.",
                "hook_seed": "Lý do bạn cứ đâm đầu vào một mối quan hệ độc hại hay một công việc rách nát.",
                "cliffhanger": "Khi đã bóc trần được nỗi sợ mất mát, công thức tối thượng để ra quyết định tỉnh táo là gì? Lời giải ở Tập 4.",
                "scenes": [
                    {"query": "red downwards financial stock market chart reflection eyes", "duration": 6.0},
                    {"query": "person holding head in hands looking at negative balance", "duration": 6.5},
                    {"query": "tearing up losing lottery ticket or failed investment paper", "duration": 5.5},
                    {"query": "sitting alone in empty dark cafe rain outside window", "duration": 6.5},
                    {"query": "deep breath looking at hand letting go of heavy stones", "duration": 6.0},
                    {"query": "cutting off toxic phone notification muting chat group", "duration": 6.0},
                    {"query": "standing firm and walking away from bad situation", "duration": 6.5},
                    {"query": "writing clear balance sheet pros and cons on fresh paper", "duration": 6.0},
                    {"query": "calm composed analytical face staring into camera", "duration": 6.0},
                    {"query": "clean bright sunrise horizon walking forward with clarity", "duration": 6.5}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn bẩy căn tính: Khung tham chiếu và làm chủ tư duy phản biện",
                "pain_focus": "Hiệu ứng đóng khung (Framing Effect): Cách một vấn đề được diễn đạt quyết định cách bạn phản ứng; người làm chủ cuộc đời là người tự đặt ra khung nhìn thay vì để truyền thông và xã hội áp đặt.",
                "hook_seed": "Cách bạn nhìn nhận thất bại chính là thứ quyết định bạn là người thắng hay kẻ thua.",
                "cliffhanger": "Hãy xem lại từ tập 1 để lập trình lại tư duy não bộ của bạn, cuốn sách khoa học kinh điển này đang có ở bình luận ghim.",
                "scenes": [
                    {"query": "antique ornate picture frame hanging in modern minimalist gallery", "duration": 6.5},
                    {"query": "looking through camera viewfinder framing city architecture", "duration": 6.0},
                    {"query": "turning upside down chess board examining new angle", "duration": 6.5},
                    {"query": "closing heavy classic science psychology book thoughtfully", "duration": 6.0},
                    {"query": "deep thoughtful breath standing high above foggy metropolis", "duration": 6.5},
                    {"query": "warm sunlight striking steady confident eyes directly", "duration": 6.0},
                    {"query": "walking calmly past chaotic flashing billboards downtown", "duration": 6.5},
                    {"query": "hands clasped calmly behind back walking steady pace", "duration": 6.0},
                    {"query": "golden morning light bathing library reading desk", "duration": 6.0},
                    {"query": "silhouette walking into clear bright blue horizon victory", "duration": 6.5}
                ]
            }
        ]
    }

    ,
    {
        "series_slug": "xa_hoi_met_moi",
        "book_title": "Xã Hội Mệt Mỏi (The Burnout Society)",
        "author": "Byung-Chul Han",
        "category": "Triết Học Đương Đại & Gen Z",
        "shopee_aff_link": "https://s.shopee.vn/60SmInZ2UG",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú tát thức tỉnh: Cái bẫy tự do và sự tự bóc lột thời đại số",
                "pain_focus": "Không ai dí súng vào đầu bạn bắt cày cuốc, chính bạn tự biến mình thành tên cai ngục tàn nhẫn nhất của chính mình; bạn bóc lột bản thân dưới danh nghĩa 'phấn đấu' và 'tự do'.",
                "hook_seed": "Điều tàn nhẫn nhất là bạn đang tự tay bóc lột chính mình... rồi gọi đó là đam mê!",
                "cliffhanger": "Nhưng tại sao chúng ta không thể ngừng lại dù cơ thể đã kiệt quệ? Bí mật nằm ở Tập 2...",
                "scenes": [
                    {"query": "tired young person working late laptop bed dark room 2am", "duration": 6.5},
                    {"query": "fluorescent lights flickering in empty endless corporate office", "duration": 6.0},
                    {"query": "rubbing exhausted eyes looking at glowing phone screen", "duration": 6.5},
                    {"query": "heartbeat monitor sound fast shallow breathing stress", "duration": 6.0},
                    {"query": "shadow of person pulling own heavy chains silhouette", "duration": 6.5},
                    {"query": "standing in moving subway train surrounded by dead-eyed commuters", "duration": 6.0},
                    {"query": "closing laptop screen shut in quiet desperation dark room", "duration": 6.5},
                    {"query": "looking out at rainy city lights sighing deeply exhaustion", "duration": 6.0},
                    {"query": "taking off watch placing it on bedside table slowly", "duration": 6.0},
                    {"query": "sitting still in darkness listening to silence", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh giới thực chiến: Cái chết của sự buồn chán sâu sắc",
                "pain_focus": "Não bộ hiện đại mất khả năng ở một mình trong tĩnh lặng; rảnh rỗi 3 giây là rút điện thoại lướt short video; sự buồn chán sâu sắc - cái nôi của sáng tạo - đã bị hủy diệt hoàn toàn.",
                "hook_seed": "Lý do bạn không thể ngồi yên 5 phút mà không rút điện thoại ra...",
                "cliffhanger": "Khi dopamine rẻ tiền đã nuốt chửng sự tập trung, căn bệnh trầm cảm thế hệ mới sẽ dẫn bạn về đâu? Sự thật ở Tập 3...",
                "scenes": [
                    {"query": "scrolling phone screen compulsively in coffee shop elevator", "duration": 6.5},
                    {"query": "chaotic fast montage flashing short video screens colorful", "duration": 6.0},
                    {"query": "vacant glazed look of person scrolling in bed night", "duration": 6.5},
                    {"query": "dust motes dancing in quiet sunbeam empty wooden room", "duration": 6.0},
                    {"query": "hand putting phone inside drawer and locking it shut", "duration": 6.5},
                    {"query": "sitting on quiet wooden porch watching rain fall steady", "duration": 6.0},
                    {"query": "deep chest breath feeling weight of silence peaceful", "duration": 6.5},
                    {"query": "single green leaf swaying gently in slow summer breeze", "duration": 6.0},
                    {"query": "looking into distance without checking device calm face", "duration": 6.5},
                    {"query": "ripples spreading slowly on tranquil mountain lake surface", "duration": 6.0}
                ]
            }
            ,
            {
                "episode": 3,
                "sub_angle": "Bóc trần mặt tối: Bẫy 'chữa lành' và ảo tưởng tích cực độc hại",
                "pain_focus": "Xã hội nhồi sọ bạn phải luôn lạc quan, tích cực; nỗi đau bị xem là bệnh tật cần giấu kín; nhưng càng ép mình 'chữa lành' bằng tiêu dùng rẻ tiền, bạn càng rơi vào khủng hoảng sâu hơn.",
                "hook_seed": "Bẫy chữa lành chính là liều thuốc độc ngọt ngào nhất bạn đang uống mỗi ngày.",
                "cliffhanger": "Vậy làm thế nào để thoát khỏi vòng xoáy kiệt sức mà không cần bỏ việc lên núi? Lời giải ở Tập 4.",
                "scenes": [
                    {"query": "fake smile breaking down into tears in bathroom mirror", "duration": 6.5},
                    {"query": "social media post with inspirational quote scrolling past", "duration": 6.0},
                    {"query": "shopping bags piling up on floor impulse purchases empty", "duration": 6.5},
                    {"query": "walking alone along windy deserted winter beach cold", "duration": 6.0},
                    {"query": "tearing down colorful self help sticky notes from wall", "duration": 6.5},
                    {"query": "stepping barefoot on cool wooden floor grounded calm", "duration": 6.0},
                    {"query": "drinking warm cup of tea both hands quiet morning", "duration": 6.5},
                    {"query": "looking honestly at raw emotion in mirror without judgment", "duration": 6.0},
                    {"query": "taking a long slow breath accepting imperfection", "duration": 6.5},
                    {"query": "morning mist clearing over still pine forest sunrise", "duration": 6.0}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn bẩy giải phóng: Nghệ thuật nói 'KHÔNG' và sống chậm lại",
                "pain_focus": "Sức mạnh tối thượng của Byung-Chul Han: Khả năng nói KHÔNG với những đòi hỏi vô độ của xã hội hiệu suất; dám sống vô dụng một chút để bảo toàn linh hồn và sự tỉnh thức.",
                "hook_seed": "Dũng cảm lớn nhất của đời bạn là dám buông bỏ cuộc đua không có hồi kết.",
                "cliffhanger": "Hãy xem lại từ tập 1 để thức tỉnh khỏi cơn ác mộng kiệt sức, cuốn sách triết học gối đầu giường đang nằm ở bình luận ghim.",
                "scenes": [
                    {"query": "walking slowly in opposite direction of rushing crowd street", "duration": 6.5},
                    {"query": "closing thick book with quiet reverence warm room", "duration": 6.0},
                    {"query": "standing still on open hill breeze rustling grass golden", "duration": 6.5},
                    {"query": "calm serene face of person truly at peace with self", "duration": 6.0},
                    {"query": "open palm catching soft falling rain drop peaceful", "duration": 6.5},
                    {"query": "sitting quietly by old wooden bookshelf reading slowly", "duration": 6.0},
                    {"query": "warm smile looking straight ahead with unshakable clarity", "duration": 6.5},
                    {"query": "silhouette walking toward peaceful sunset mountain valley", "duration": 6.0},
                    {"query": "vast open starry night sky twinkling above silence", "duration": 6.5},
                    {"query": "slow steady footsteps on ancient stone path into dawn", "duration": 6.0}
                ]
            }
        ]
    }
    ,
    {
        "series_slug": "cha_giau_cha_ngheo",
        "book_title": "Cha Giàu Cha Nghèo (Rich Dad Poor Dad)",
        "author": "Robert Kiyosaki",
        "category": "Tài Chính Cá Nhân & Tư Duy Dòng Tiền",
        "shopee_aff_link": "https://s.shopee.vn/7fb0HrSh6k",
        "episodes": [
            {
                "episode": 1,
                "sub_angle": "Cú tát thức tỉnh: Cái bẫy vòng chuột (Rat Race) và bi kịch lương cao",
                "pain_focus": "Học giỏi, bằng cấp cao, đi làm công ty lớn... nhưng tài khoản cuối tháng vẫn về số 0; lương tăng từ 10 triệu lên 30 triệu thì chi tiêu tăng theo; bạn đang quay cuồng trong cái bẫy vòng chuột.",
                "hook_seed": "Lương tăng gấp ba mà tài khoản vẫn rỗng... Bạn đang rơi vào cái bẫy nguy hiểm nhất!",
                "cliffhanger": "Nhưng bí mật mà trường học không bao giờ dạy bạn về đồng tiền là gì? Sự thật ở Tập 2...",
                "scenes": [
                    {"query": "hamster running frantically on plastic wheel close up", "duration": 6.0},
                    {"query": "crowd of office workers walking head down in subway morning", "duration": 6.5},
                    {"query": "bank account notification showing salary deposited then drained", "duration": 6.0},
                    {"query": "tired man calculating bills on kitchen table late night", "duration": 6.5},
                    {"query": "signing credit card receipt for luxury brand purchase regret", "duration": 6.0},
                    {"query": "stepping out of office elevator into cold night air alone", "duration": 6.5},
                    {"query": "tearing up credit card statement with firm determination", "duration": 6.0},
                    {"query": "looking at hands realizing need for fundamental change", "duration": 6.5},
                    {"query": "sitting upright taking deep breath opening finance notebook", "duration": 6.0},
                    {"query": "city skyline lights glittering through dark window glass", "duration": 6.5}
                ]
            },
            {
                "episode": 2,
                "sub_angle": "Ranh giới thực chiến: Phân biệt tài sản và tiêu sản",
                "pain_focus": "Quy tắc vàng của Kiyosaki: Người giàu mua tài sản (bỏ tiền vào túi), người nghèo mua tiêu sản (rút tiền khỏi túi) nhưng lầm tưởng đó là tài sản. Chiếc xe trả góp hay căn nhà nợ ngập đầu thực chất là gì?",
                "hook_seed": "Căn nhà bạn đang trả góp hai mươi năm... KHÔNG PHẢI TÀI SẢN CỦA BẠN!",
                "cliffhanger": "Nếu căn nhà là tiêu sản, vậy thứ gì mới thực sự tạo ra dòng tiền nuôi sống bạn suốt đời? Khám phá ở Tập 3...",
                "scenes": [
                    {"query": "luxury sports car in showroom keys dangling gleaming", "duration": 6.0},
                    {"query": "hand writing formula Asset vs Liability on whiteboard", "duration": 6.5},
                    {"query": "two columns comparing cash inflow vs cash outflow paper", "duration": 6.0},
                    {"query": "counting crisp currency banknotes on desk methodical", "duration": 6.5},
                    {"query": "firm resolute expression rejecting expensive impulsive purchase", "duration": 6.0},
                    {"query": "investing in index fund or real estate contract signature", "duration": 6.5},
                    {"query": "calm confident person drinking coffee reading financial report", "duration": 6.0},
                    {"query": "green upward trending chart graph on laptop screen clear", "duration": 6.5},
                    {"query": "walking past luxury shopping mall windows without glancing", "duration": 6.0},
                    {"query": "modern glass architecture skyscraper gleaming in sunlight", "duration": 6.5}
                ]
            }
            ,
            {
                "episode": 3,
                "sub_angle": "Bóc trần mặt tối: Người nghèo làm việc vì tiền, người giàu bắt tiền làm việc",
                "pain_focus": "Nỗi sợ mất việc và lòng tham tiêu dùng khiến 95% con người cam chịu làm nô lệ cho đồng tiền; người giàu đầu tư thời gian xây dựng hệ thống dòng tiền thụ động để giải phóng chính mình.",
                "hook_seed": "Chăm chỉ làm thuê không bao giờ giúp bạn giàu, nó chỉ giúp sếp của bạn giàu.",
                "cliffhanger": "Khi đã hiểu quy luật dòng tiền, bước đi dứt điểm nào giúp bạn bước ra khỏi vòng chuột? Lời giải ở Tập 4.",
                "scenes": [
                    {"query": "alarm clock blaring 6am exhausted hand reaching out", "duration": 6.0},
                    {"query": "finger typing numbers furiously into spreadsheet corporate", "duration": 6.5},
                    {"query": "gears of antique brass clock turning relentlessly macro", "duration": 6.0},
                    {"query": "person looking at office badge hanging around neck sigh", "duration": 6.5},
                    {"query": "taking off company badge placing it on wooden desk resolute", "duration": 6.0},
                    {"query": "drawing business model canvas ecosystem flowchart paper", "duration": 6.5},
                    {"query": "small green plant sprouting from pile of gold coins macro", "duration": 6.0},
                    {"query": "walking with quiet power and purposeful stride downtown", "duration": 6.5},
                    {"query": "warm smile of entrepreneur holding cup looking at sunrise", "duration": 6.0},
                    {"query": "ocean cargo ship moving steady across open sea horizon", "duration": 6.5}
                ]
            },
            {
                "episode": 4,
                "sub_angle": "Đòn bẩy giải phóng: Vượt qua nỗi sợ và xây dựng trí thông minh tài chính",
                "pain_focus": "Sự khác biệt duy nhất giữa người giàu và người nghèo là cách họ đối diện với nỗi sợ mất tiền. Kẻ hèn nhát chọn an toàn để rồi chết chìm trong lạm phát; người bản lĩnh học cách quản trị rủi ro để giành lấy tự do.",
                "hook_seed": "Nếu sợ mất tiền, bạn đã cầm chắc bản án nghèo khó cả đời.",
                "cliffhanger": "Hãy xem lại từ tập 1 để cài đặt lại hoàn toàn tư duy tài chính, cuốn sách vỡ lòng của triệu phú đang nằm ở bình luận ghim.",
                "scenes": [
                    {"query": "rock climber leaping across wide chasm catching ledge firm", "duration": 6.5},
                    {"query": "closing classic rich dad poor dad purple book with satisfaction", "duration": 6.0},
                    {"query": "deep steady breath standing on balcony overlooking vast city", "duration": 6.5},
                    {"query": "calm confident eyes filled with unwavering financial clarity", "duration": 6.0},
                    {"query": "opening curtains letting bright morning sun flood living room", "duration": 6.5},
                    {"query": "walking along tranquil beach at dawn fresh ocean breeze", "duration": 6.0},
                    {"query": "hand firmly shaking partner hand closing profitable venture", "duration": 6.5},
                    {"query": "genuine relaxed smile of true financial freedom and peace", "duration": 6.0},
                    {"query": "standing tall on mountain peak golden sunrise spreading vast", "duration": 6.5},
                    {"query": "silhouette walking boldly into bright dawn of limitless future", "duration": 6.0}
                ]
            }
        ]
    }
]
