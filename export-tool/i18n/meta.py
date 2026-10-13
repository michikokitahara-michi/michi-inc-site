"""Per-language strings used by export.py (titles, descriptions, UI texts)."""
HTML_LANG = {'ja': 'ja', 'en': 'en', 'fr': 'fr', 'ko': 'ko', 'zh': 'zh-Hans'}
OG_LOCALE = {'ja': 'ja_JP', 'en': 'en_US', 'fr': 'fr_FR', 'ko': 'ko_KR', 'zh': 'zh_CN'}
LABEL = {'ja': '日本語', 'en': 'English', 'fr': 'Français', 'ko': '한국어', 'zh': '简体中文'}
SHORT = {'ja': 'JA', 'en': 'EN', 'fr': 'FR', 'ko': 'KO', 'zh': 'ZH'}
LANG_ARIA = {'ja': '言語', 'en': 'Language', 'fr': 'Langue', 'ko': '언어', 'zh': '语言'}
NEW_TAB = {'en': ' (opens in a new tab)', 'fr': ' (s’ouvre dans un nouvel onglet)', 'ko': ' (새 탭에서 열림)', 'zh': '（在新标签页中打开）'}
SENDING = {'en': ('Sending…', 'Send'), 'fr': ('Envoi…', 'Envoyer'), 'ko': ('보내는 중…', '보내기'), 'zh': ('提交中…', '提交')}
FORM_ERR = {
    'en': 'Your message could not be sent. Please try again later, or email michiko.kitahara@michi-inc.com directly.',
    'fr': 'Votre message n’a pas pu être envoyé. Veuillez réessayer plus tard ou écrire directement à michiko.kitahara@michi-inc.com.',
    'ko': '전송하지 못했습니다. 잠시 후 다시 시도하시거나 michiko.kitahara@michi-inc.com 으로 직접 연락해 주세요.',
    'zh': '提交失败。请稍后重试，或直接发送邮件至 michiko.kitahara@michi-inc.com。',
}
FONTS = {  # replace Japanese web fonts for CJK languages
    'ko': {'Shippori Mincho': 'Noto Serif KR', 'Zen Kaku Gothic New': 'Noto Sans KR'},
    'zh': {'Shippori Mincho': 'Noto Serif SC', 'Zen Kaku Gothic New': 'Noto Sans SC'},
}
TITLES = {
    'en': {'index.html': 'MICHI inc. | Connecting the dots, creating paths yet unknown', 'company.html': 'Company | MICHI inc.', 'privacy.html': 'Privacy Policy | MICHI inc.'},
    'fr': {'index.html': 'MICHI inc. | Relier les points, tracer des chemins encore inconnus', 'company.html': 'Entreprise | MICHI inc.', 'privacy.html': 'Politique de confidentialité | MICHI inc.'},
    'ko': {'index.html': 'MICHI inc. | DOT을 잇고, 미지의 길을 만든다', 'company.html': '회사 개요 | MICHI inc.', 'privacy.html': '개인정보 처리방침 | MICHI inc.'},
    'zh': {'index.html': 'MICHI inc. | 连接每一个点，开创未知之路', 'company.html': '公司概况 | MICHI inc.', 'privacy.html': '隐私政策 | MICHI inc.'},
}
DESC = {
    'en': 'MICHI inc. is a brand creation studio in Tokyo that connects the dots of people, companies and communities that strive to grow — creating brands, designing brand experiences and growing organizations. CEO: Michiko Kitahara.',
    'fr': 'MICHI inc. est un studio de création de marques à Tokyo qui relie les points des personnes, des entreprises et des territoires qui veulent grandir : créer des marques, concevoir des expériences de marque et faire grandir les organisations. CEO : Michiko Kitahara.',
    'ko': 'MICHI inc.(주식회사 MICHI)는 성장하려는 사람과 기업, 지역의 점을 이어 브랜드 창조, 브랜드 경험 설계, 조직 만들기를 함께하는 도쿄의 브랜드 크리에이션 스튜디오입니다. 대표이사 CEO 기타하라 미치코.',
    'zh': 'MICHI inc.（株式会社MICHI）是位于东京的品牌创造工作室，连接努力成长的人、企业与地区的点，陪伴客户创造品牌、设计品牌体验、培育组织。CEO：北原规稚子。',
}
PAGE_DESC = {
    'en': {
        'concept.html': 'The vision, concept and services of MICHI inc.: before "how to sell," create "the core value." We create brands, deliver brand experiences and grow organizations through brands.',
        'about.html': 'Profile of Michiko Kitahara, CEO of MICHI inc. After building brands at Lion and Shiseido, where she served as Deputy CMO, she founded MICHI inc. in 2025. She also serves as an outside director and lecturer.',
        'works.html': 'Selected works of MICHI inc.: branding and marketing support, talks and more.',
        'media.html': 'Media coverage and appearances of Michiko Kitahara, CEO of MICHI inc. — articles, interviews, TV and video.',
        'talks.html': 'Talks and speaking engagements by Michiko Kitahara, CEO of MICHI inc., including ad:tech tokyo, Nikkei Cross Trend Forum and MarkeZine Day.',
        'contact.html': 'Contact MICHI inc. for branding and marketing support, talks, training and workshops.',
        'company.html': 'Company information of MICHI inc. (MICHI Co., Ltd.): representative, founding date, address (Kita-Aoyama, Minato-ku, Tokyo) and business.',
        'privacy.html': 'Privacy policy of MICHI inc. (MICHI Co., Ltd.).',
    },
    'fr': {
        'concept.html': 'La vision, le concept et les services de MICHI inc. : avant « comment vendre », créer « la valeur essentielle ». Créer des marques, offrir des expériences de marque et faire grandir les organisations par la marque.',
        'about.html': 'Profil de Michiko Kitahara, CEO de MICHI inc. Après avoir construit des marques chez Lion et Shiseido, où elle a été Deputy CMO, elle a fondé MICHI inc. en 2025. Elle est aussi administratrice indépendante et intervenante.',
        'works.html': 'Réalisations de MICHI inc. : accompagnement en branding et marketing, conférences et plus.',
        'media.html': 'Presse et apparitions médias de Michiko Kitahara, CEO de MICHI inc. : articles, entretiens, télévision et vidéo.',
        'talks.html': 'Conférences et interventions de Michiko Kitahara, CEO de MICHI inc., dont ad:tech tokyo, Nikkei Cross Trend Forum et MarkeZine Day.',
        'contact.html': 'Contactez MICHI inc. pour un accompagnement en branding et marketing, des conférences, des formations et des ateliers.',
        'company.html': 'Informations sur MICHI inc. (MICHI Co., Ltd.) : représentante, date de création, adresse (Kita-Aoyama, Minato-ku, Tokyo) et activités.',
        'privacy.html': 'Politique de confidentialité de MICHI inc. (MICHI Co., Ltd.).',
    },
    'ko': {
        'concept.html': '‘어떻게 팔 것인가’ 이전에 ‘핵심 가치’를 만든다. MICHI inc.의 비전과 콘셉트, 그리고 브랜드를 만들고, 브랜드 경험을 전하고, 브랜드로 성장하는 조직을 키우는 세 가지 서비스를 소개합니다.',
        'about.html': '주식회사 MICHI 대표이사 CEO 기타하라 미치코의 프로필. 라이온과 시세이도에서 브랜드를 만들었고, 시세이도에서는 부CMO 등을 역임. 2025년 MICHI inc.를 설립했으며 사외이사와 강사로도 활동하고 있습니다.',
        'works.html': 'MICHI inc.의 브랜딩·마케팅 지원, 강연 등의 실적입니다.',
        'media.html': 'MICHI inc. 대표이사 CEO 기타하라 미치코의 미디어 게재·출연(기사, 인터뷰, TV, 영상 등) 목록입니다.',
        'talks.html': '기타하라 미치코(MICHI inc. 대표이사 CEO)의 강연·출연 정보. ad:tech tokyo, 닛케이 크로스 트렌드 포럼, MarkeZine Day 등.',
        'contact.html': '브랜딩·마케팅 지원, 강연·연수·워크숍 의뢰 등 MICHI inc.에 대한 문의는 이곳에서.',
        'company.html': '주식회사 MICHI(MICHI inc.)의 회사 개요. 대표자, 설립, 소재지(도쿄도 미나토구 기타아오야마), 사업 내용을 안내합니다.',
        'privacy.html': '주식회사 MICHI(MICHI inc.)의 개인정보 처리방침.',
    },
    'zh': {
        'concept.html': '在“怎么卖”之前，先创造“核心价值”。介绍MICHI inc.的愿景、理念，以及创造品牌、传递品牌体验、培育借助品牌成长的组织三项服务。',
        'about.html': '株式会社MICHI CEO 北原规稚子简介。曾在狮王与资生堂打造品牌，在资生堂历任副CMO等职。2025年创立MICHI inc.，同时担任独立董事与讲师。',
        'works.html': 'MICHI inc.的品牌与营销支持、演讲等业绩。',
        'media.html': 'MICHI inc. CEO 北原规稚子的媒体报道与出演（文章、专访、电视、视频等）。',
        'talks.html': '北原规稚子（MICHI inc. CEO）的演讲与出演信息，包括ad:tech tokyo、日经Cross Trend Forum、MarkeZine Day等。',
        'contact.html': '品牌与营销支持、演讲、研修及工作坊等，欢迎通过此页面联系MICHI inc.。',
        'company.html': '株式会社MICHI（MICHI inc.）公司概况：代表人、成立时间、地址（东京都港区北青山）及业务内容。',
        'privacy.html': '株式会社MICHI（MICHI inc.）隐私政策。',
    },
}
for _l in PAGE_DESC: PAGE_DESC[_l]['index.html'] = DESC[_l]
