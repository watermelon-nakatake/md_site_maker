// 例文
const labelArray = {
    '0': ['出会いの目的', '彼女探し', '婚活', 'メル友探し', 'セフレ探し', '早く会える女性探し'],
    '1': ['相手からのメールの内容', '質問に答えてくれた', '質問に答えずに別の質問してきた', 'そっけない一言メール'],
    '2': ['出会いの目的', '彼女探し', '婚活', 'メル友探し', 'セフレ探し', '早く会える女性探し'],
    '3': ['連絡先交換する口実', 'もっと話がしたいから', 'ラインの方が便利だから', 'ポイントがないから'],
    '4': ['会おうと誘う口実', '映画に誘う', '食事に誘う', '飲みに誘う', '仕事で行くついでに誘う'],
    '5': ['会話の話題', 'お酒の話', '好きな本の話', '音楽の話', '恋愛の話', '好きな食べ物の話', 'ゲームの話'],
    '6': ['プロフィールのタイプ', '彼女募集', '遊べる女友達やセフレ募集', '切実な彼女募集', 'オールマイティ']
};
const firstMail = {0: 'f00', 1: 'f01', 2: 'f02', 3: 'f03', 4: 'f04'};
const secondMail = {0: 's00', 1: 's01', 2: 's02'};
const post = {0: 'p00', 1: 'p01', 2: 'p02', 3: 'p03', 4: 'p04'};
const address = {0: 'a00', 1: 'a01', 2: 'a02'};
const dateMail = {0: 'd00', 1: 'd01', 2: 'd02', 3: 'd03'};
const profile = {0: 'i00', 1: 'i01', 2: 'i02', 3: 'i03'};
const mailList = [firstMail, secondMail, post, address, dateMail, '', profile];
const mailTextList = {
    f00: 'はじめまして、(herName)。$$$(自己紹介)いろんなことを一緒に楽しめる彼女が欲しくて、このサイトに登録しました。$$$' +
        '(herName)のプロフィールを見て、素敵な人だなと思ったのでメールを送ってみました。$$' +
        'まずはメールからゆっくり仲良くなれたら嬉しいです。$$$' +
        '(option1)$$$では、お返事待ってますね。' +
        '[敬語を使って書くことで、誠実な人だという印象を与えます。$$また、相手を褒めることでこちらの印象をよくすることができます。',
    f01: 'はじめまして、(herName)。$$$(自己紹介)将来のことを考えられるような女性との出会いを探しています。$$$' +
        '(herName)のプロフィールを見て、とても素敵な方だなと感じてご連絡差し上げました。$$' +
        'まずはメールでいろいろお話しできたらと思います。$$$' +
        '(option1)$$$では、お返事待ってますね。',
    f02: 'はじめまして、(herName)。$$$(自己紹介)実際に会うとかは考えずに純粋にメールのやりとりを楽しめるメル友を探しています。$$$' +
        '(herName)のプロフィールを見て、お話しするのが楽しそうだなと思ったのでメールさせてもらいました。$$' +
        '是非(自分)のメル友になってください。$$$' +
        '(option1)$$$では、期待してお返事お待ちします。',
    f03: 'はじめまして、(herName)。$$$(自己紹介)彼女とかではなくて、一緒にいろいろ楽しめるような女性との出会いを探しています。$$$' +
        '(herName)のプロフィールを見て、とても素敵な方だなと思ったのでメッセージ送ってみました。$$' +
        'まずはメールでいろいろお話しして、仲良くなったら遊んだり、お酒を飲んだりしましょう。$$$' +
        '(option1)$$$では、お返事待ってますね。',
    f04: 'はじめまして、(herName)。$$$(自己紹介)彼女とかじゃなくて、お互い都合がいいときにちょっと遊んだりできるような' +
        '相手を探してます。$$$' +
        '(herName)のプロフィールを見て、とてもいい感じの人だなと思ったのでメッセージ送ってみました。$$' +
        'まずはメールでいろいろお話しして、仲良くなったら遊んだり、お酒を飲んだりしましょう。$$$' +
        '(option1)$$$では、お返事を超期待して待ってますね！',
    s00: '(herName)、(option2)。$$$メールありがとうございます。$$' +
        '(herName)とはぜひ仲良くなりたいと思っていたので、とても嬉しいです。$$' +
        'これからよろしくお願いしますね。$$仲良くしてくださいね。$$$(option3)',
    s01: '(herName)、(option2)。$$$返信ありがとうございます。$$' +
        '(herName)とはぜひお話ししてみたいと思っていたので、とても嬉しいです。$$' +
        'これからよろしくお願いしますね。$$$(以下、相手からの質問への回答とその質問に関係するこちらからの新しい質問)',
    s02: '(herName)、(option2)。$$$返信ありがとうございます。$$(herName)からお返事をもらえてすごく嬉しいです。$$' +
        'これからよろしくお願いしますね。$$$(option1)',
    p00: '書き込みを見てくださってありがとうございます。$$$' +
        '仲の良い友達からは「お前に彼女がいないのはおかしい」とか言われるけど、心から大事にできる人とお付き合いしたいと思っているので' +
        'なかなかいい出会いがありません。$$$' +
        'ということで、真面目にお付き合いできる女性を探してます。$$メールからゆっくり仲良くなれたら嬉しいです。$$$' +
        '少し自己紹介しますね。$$(自己紹介)' +
        '普段仕事が忙しいので、休みの日とかは体を動かしたり美味しいものを食べたりしてストレス解消しています。$$$' +
        'では、気になる方はお気軽にメールくださいね。$$$' +
        'いい方と出会えたらこの書き込みは消しますのでお急ぎください（笑）',
    p01: '書き込みを見てくださってありがとうございます。$$$(自己紹介)' +
        '年齢的に最近結婚のことも考えるようになってきたので、将来のことも考えられるような素敵な女性との出会いを探しています。$$$' +
        'かなり真剣です。$$$' +
        '優しくて一緒にいろいろなことにチャレンジできるような女性が好きなので、そういう方と知り合えたら嬉しいです。$$' +
        'まずはメールからゆっくりお話しして、仲良くなりましょう。$$$' +
        '本気でお付き合いできる方と知り合えたら、この書き込みは消しますね。$$$メールお待ちしています。',
    p02: '書き込みを見てくださってありがとうございます。$$$' +
        '純粋にメールだけでやり取りして会話を楽しめる女性のメール友達が欲しくて書き込みをしました。$$$' +
        '(趣味)が好きなので、(趣味)についていろいろ語り合えるようなメル友さんができるととても嬉しいです。$$' +
        'もちろん(趣味)に興味ない方でもOKです。$$$' +
        '「会おう」とかは絶対に言わないので、安心してメールしてきてくださいね。',
    p03: '書き込み見てくださってありがとうございます。$$$' +
        '彼女を探しているというわけではないんですが、一緒に遊んだり美味しいものを食べたり、' +
        'その他のことも楽しめる素敵な女性を探してます。$$$' +
        '(自分)は女性に喜んでもらうのが好きなので、いい意味でかなり尽くしますよ！$$$' +
        '年齢は気にしないけど、あまりぽっちゃりし過ぎてなくて優しい女性が好きですね。$$$' +
        '気になった方は、お気軽にメールをお送りください。$$期待して待ってます！',
    p04: '最近仕事をがんばり過ぎて、ちょっと疲れがたまってます。$$こんな時は美味しいお酒と食事で疲れを吹き飛ばしたい･･･。$$$' +
        '美味しい料理とお酒が大好きな女の子、いらっしゃったらメールで教えてください！$$$' +
        '(自分)と飲みに行きましょう！$$$行きたいお店があればそこでもいいですし、特になければ(自分)のおすすめのお店でご馳走します。$$$' +
        'お時間はそちらの都合に合わせますよ。$$$楽しい飲み会にしたいですね。',
    a00: '(herName)とお話しするのすごく楽しいです。$$もっとたくさんお話ししたいので、' +
        '(herName)さえ良ければ連絡先を交換して直接やりとりしませんか？$$$' +
        'ラインIDでも携帯とかのメールアドレスでもどっちでもいいですよ。$$でも、嫌な時はもう少しサイト内でメールするから言ってくださいね。',
    a01: '(herName)とメールするの、すごく楽しいです。$$(herName)とは気が合いそうです。$$$' +
        'もし大丈夫なら、ラインIDとかメアド交換して、直接やり取りしませんか？$$$' +
        'その方がサイト経由でメールするよりスムーズにやり取りできますし。$$$' +
        'もちろん、知り合ったばかりでまだ早いと(herName)が思うなら、まだ全然大丈夫ですよ！',
    a02: 'ごめんなさい。$$$' +
        '(herName)とメールするのすごく楽しいからもっとメールしていたいんだけど、ポイントがなくなったからしばらくメールできません。$$' +
        'ポイントを買い足したら、またすぐメールしますね。$$$ひょっとしたら少し時間がかかるかも知れないけど･･･。$$$' +
        'それか、(自分)LINE使ってるのでそっちの方ならすぐにまたお返事できると思います。$$$念のためIDを教えておきますね。$$$' +
        '(oi自分のラインID) です。' +
        '[この聞き方は、「ポイントがない ＝ お金がない」でマイナスイメージを与える場合があるのであまりおすすめしません。$$' +
        'もしダメになってもいい相手に対して、最後の１通で送る時などに利用すると良いと思います。',
    d00: '(herName)、来週の金曜日の夜とか空いてます？$$$もしご都合が良ければ一緒に映画観に行きませんか？$$$' +
        '(herName)が観たいって言ってた(oi映画の作品名)観に行きましょう！',
    d01: '(herName)、この間のメールで(oi相手の好きな食べ物)好きだって言ってましたよね？$$$' +
        '(oi相手の好きな食べ物)の美味しいお店があるんですけど、(herName)、一緒に食べに行きませんか？$$$' +
        '前から(自分)も行ってみたいって思ってたんですけど、なかなか一緒に行ってくれる友達がいなくって。',
    d02: '(herName)、来週の金曜日の夜って何か予定入ってます？$$$' +
        '(自分)ここ最近仕事が忙しかったんですけど、それがやっと終わって自分的に打ち上げしたい気分なんです。$$$' +
        'もし(herName)さえよければ、一緒にお酒飲みたいなと思って。$$$' +
        'お店は、この間見つけた美味しそうな(oi相手が好きな料理)のお店を考えてます。$$$' +
        'ご都合どうですか？もちろんご馳走しますよ（笑）',
    d03: '今度の金曜日、仕事で(oi相手の住んでいるor職場の地名)に行くことになりました。$$' +
        'そのまま直帰するんですけど、せっかくだから、もし良かったら一緒にご飯でも食べませんか？$$$' +
        '(herName)おすすめの美味しいお店とかあったらぜひ教えてください！' +
        '[これは意外に成功しやすい誘い方です。$$' +
        '本当で仕事で行く用事があればベストですが、もしもなくても仕事で行くということにして誘ってOKです。',
    i00: 'はじめまして！$$$(自己紹介)$$$' +
        'お休みの日に一緒に出かけたりできる彼女が欲しいと思って、こちらに登録しました。$$$(option5)$$$' +
        'まずはメールとかでゆっくりお話しして、仲良くなったらご飯を食べに行ったりしましょう。$$' +
        '気軽に(access)してくださいね！' +
        '[簡単な自己紹介の後に、やわらかめのコメントを入れて、読んだ女性がメールや「いいね」をしたい気持ちにさせるようにしています。$$' +
        '自分に当てはまるものを選んでください。$$$別に5秒で店を選んだり、観光地を知らなくてもなんとかなるので全く問題ありません。',
    i01: 'プロフィール閲覧ありがとうございます。$$(自己紹介)$$女性の友達が欲しくてこのサイトに登録しました。$$$' +
        '学生時代とかにはある程度女友達もいたんですけど、社会人になって仕事が忙しいのもあって疎遠になってしまいました。$$' +
        '気軽に食事とかアウトドア系の遊びなんかを一緒に楽しめる女友達が作れたら嬉しいです。$$$' +
        'やましいこととかは全く考えてないので、安心して(access)してくださいね。(笑)$$200%お返事します！！' +
        '[「やましい事はしない」と書いていますが、やましいことを考えているのは「いいね」やメールしてくる相手の女性も了解済みです。',
    i02: 'はじめまして！$$(自己紹介)$$$3年前に彼女と別れてから、彼女がいません。$$' +
        '仕事が忙しく、出会いの場に行く機会もなく、ここまで過ごしてき他のですが、最近になって少し仕事も落ち着き、' +
        'ある程度余裕ができてきたたので、彼女を募集しようと思いこちらに登録してみました。$$$' +
        'メールから恋愛関係まで至るのは簡単ではないかもしれませんが、まずは気軽にメールのやり取りをして仲良くなれたら嬉しいです。$$$' +
        '気軽に(access)してくださいね。$$お待ちしています。',
    i03: 'プロフィールを見てくださってありがとうございます！$$' +
        '(自己紹介)$$' +
        '新しい友達を作りたいと思ってこのサイトに登録しました。$$$' +
        'もう少し詳しく自己紹介しておきますね。$$(自分)は身長(pi身長)、体重(pi体重)の(pi体型)タイプです。$$' +
        '顔は芸能人の(pi似ている芸能人1)や(pi似ている芸能人2)に似ているとたまに言われたりするので、想像してみてください。$$$' +
        '性格的には(pi性格)タイプだと言われるので、一緒にいると意外と楽しいと思います。$$' +
        '(piスポーツ)とか(pi趣味)なんかが好きで、休みの日には楽しんでます。$$$' +
        '色々な方とお知り合いになれたら嬉しいです。$$気軽に(access)してくださいね！' +
        '[自分のことをとにかく紹介するタイプのプロフィールです。$$身長体重などの体型のデータはセフレを探している女性にとっては' +
        '知りたいデータなので、セフレ探しをしている女性からのアクションも期待できます。',
};
const comboList = [
    ['プロフィールに書いてあったんですけど、(herName)はお酒がお好きなんですね。$$(自分)もお酒好きです。$$$' +
    '(herName)はどんなお酒が特にお好きなんですか？',
        'お酒が好きなんですね。$$$' +
        '私はワインをよく飲んでます。',
        '(herName)、ワインがお好きなんですね。$$私もワイン好きです。$$$' +
        '(herName)、ワインは赤と白どっちがお好きですか？',
        'ワインお好きなんですか。$$気が合いそうですね。$$$' +
        '私は最近は白ワインをよく飲んでます。',
        '白ワインをよく飲まれるんですね。$$$' +
        '(自分)も白ワインが多いです。$$特に辛口をよく飲みます。$$$' +
        '私はワインの時にはチーズをよく食べてるんですけど、(herName)はどんなおつまみが好きですか？',
        '私もチーズ好きです。$$カマンベールチーズをよく食べてます。$$$' +
        'あとは、生ハムとかパスタを食べてますね。',
        'カマンベールチーズ、私もよく食べてます。$$$' +
        'あと、生ハムもいいですね。$$私はサラダに乗せて食べたりもします。$$$' +
        '(herName)、お酒好きだと結構強い方なんですか？どれくらい飲まれます？$$$' +
        'ちなみに(自分)はかなりお酒強いです。',
        '自分で料理作ったりされるんですね。$$私も料理好きです。$$$' +
        'お酒は割と強い方だと思います（笑）$$$' +
        '女子なんですけど、飲む時は一人でボトル一本空けちゃいます（笑）',
        'ボトル一本空ける時があるんですか？それはなかなかお強いですね。$$$' +
        '(自分)もワイン１本空けることあるけど、そのあとはいつの間にか寝てしまってます（笑）$$$' +
        '(herName)って、酔っぱらうとどんな感じになるんですか？甘えん坊になったりします？（笑）'],
    ['プロフィールの読書が好きって書いてありましたね。$$(自分)も本読むの好きです。$$$(herName)はどんな本をよく読まれるんですか？',
        '私はミステリーが好きです。',
        '(herName)、ミステリーがお好きなんですね。$$私もミステリー好きです。$$$ミステリーで特に好きな作家さんとかいます？',
        '綾辻行人さんが好きです。',
        '綾辻さんですか。$$いいですよね！私もよく読みます。$$$' +
        '綾辻さんの作品の中でどれが好きですか？私は絢辻さんだと、十角館の殺人が好きですね。',
        '私は時計館が好きです。',
        '時計館もいいですよね。$$$(自分)が最近ハマってるのは貫井徳郎さんです。$$(herName)、読まれました？'],
    ['プロフ読ませて頂いたんですけど、(herName)って音楽聴くのが好きなんですね。$$俺も音楽よく聴いてますよ。$$$' +
    '(herName)はどういう音楽をよく聴かれるんですか？',
        '洋楽をよく聴いてます',
        'へえ、洋楽聴いてるんですか。$$かっこいいですね。$$俺も洋楽聴いてみようかな。$$$' +
        '(herName)的にはどのアーティストが一番オススメですか？',
        'サム・スミスがいいですよ',
        'サム・スミスですね。$$了解です！近いうちに聴いてみますね。$$かなり楽しみです。$$$' +
        'サム・スミスの曲で、(herName)が特に気に入っている曲とかありますか？'],
    ['(herName)って、今彼氏いるんですか？',
        '今は彼氏いないです。',
        'そうなんですか！(herName)モテそうだから彼氏いると思ってたんですけど。$$$(自分)も今彼女いないんです。$$$' +
        'どれくらい彼氏いないんです？',
        '１年くらいかな。',
        '１年彼氏いないんですか。$$じゃあ、そろそろ寂しくなったりする頃ですね。$$$(herName)、どういうタイプの男の人が好きなんですか？',
        '優しいけど引っ張っていってくれるタイプの人が好きです。',
        '優しいのは大事ですね。$$(自分)も優しい女の人が好きです。$$$あと、自分の意見がある人がいいですね。$$$' +
        '引っ張っていってくれる人が好きってことは、(herName)って結構甘えん坊だったりするんですか？（笑）',
        'どっちかというと甘えん坊タイプかもしれないですね。$$$構ってくれないと寂しくなります（笑）',
        'やっぱりそうなんだ（笑）$$$そんな甘えん坊タイプなら、好きになったら一途なんでしょうね。$$浮気とかしたことないですよね？',
        '実は、寂しくて浮気したことあります（笑）',
        '浮気したことあるんですか？意外だな〜。$$$でも、彼氏が構ってくれなくて寂しい時は仕方ないですよね。$$$' +
        '浮気相手はどんなタイプの男性だったんですか？' +
        '[この会話例では、最後の方で浮気をしたことがあるか聞いています。$$' +
        'ここで浮気をしたことがあると答えた女性は、遊んだりセフレにするのにはベストです。$$簡単に会えると思います。$$' +
        '一方、彼女や結婚相手にするのはやめておいた方がいいでしょう。'],
    ['(herName)って、食べ物ではどんなものが好きなんですか？',
        '私は焼き鳥が好きです。',
        '焼き鳥がお好きなんですか？(自分)も焼き鳥好きです。$$$焼き鳥の中でも何か特に好きな種類ありますか？$$$(自分)はハツが好きですね。',
        'ハツ美味しいですよね。$$$私は鶏皮です。$$太っちゃいそうだけど（笑）',
        '鶏皮、いいですね。$$(自分)も焼き鳥に行ったら鶏皮は必ず食べてます。$$$コラーゲンだし、お肌にないいんじゃないですか？（笑）$$$' +
        '(herName)、特にお気に入りのお店とかありますか？',
        '焼き鳥屋さんでは○○にある○○ってお店によく行ってます。$$$あそこの鶏皮はかなり美味しいです。',
        '○○ですか。$$$美味しいとは聞いてるんですけど、(自分)まだ行ったことないんですよね。$$行ってみたいなあ。$$$' +
        'そのうち一緒に行きましょうか（笑）$$$(herName)、焼き鳥が好きってことは、お酒も好きなんですか？',
        'そうですね、そのうち一緒に行きましょう。$$$私、お酒は飲めないんです。$$$飲んだら頭痛くなっちゃって。',
        'そうなんですか。$$頭痛いのは大変ですね。$$$(自分)は飲めるけど、そんなに強くないです。$$$' +
        'じゃあ、飲み会の時はウーロン茶飲んでます？',
        '飲み会の時はあれば炭酸水ですね。$$$ジンジャーエールとかもよく飲みます。',
        '炭酸系はさっぱりしてていいですよね。$$$職場の飲み会とか、友達との女子会とか、飲み会多かったりするんですか？' +
        '[この会話例では、好きな食べ物の話題から最終的にはお酒の話題に移っています。$$大人同士の会話ではこのケースも多いです。$$' +
        '会話の中で一緒にそのうち一緒に食べに行こうと誘っていますが、これは軽く流しておいて、仲良くなってから本格的に誘いましょう。'],
    ['(herName)のプロフィールにゲームが好きって書いてあったんですけど、どんなゲームをされるんですか？',
        'ラインでツムツムやったり、ポコポコやったりしてます。',
        'ツムツムとポコポコですか。$$自分もポコポコやってます。$$まだ始めたばかりですけど。$$$' +
        'でも、なかなか進まなくなって難しいですね。$$$(herName)はポコポコ、どのくらい進んでるんですか？',
        'ステージ500台に入ったばかりですね。$$私もなかなか進みません（笑）',
        '500はすごいですよ！是非コツを教えてください。$$$そうだ、(herName)ポコポコやってるなら、ラインで友達になりましょう。$$$' +
        'もうすぐイベントとかあるので、助けてください。[最近、携帯ゲームが趣味だという女性が出会い系サイトにも増えています。$$' +
        'ラインに紐づけられている携帯ゲームだと、アイテムのやり取りなどでラインIDを教えてもらいやすかったりするので、' +
        'ゲームネタは出会いにも使えます。']

];
const optionArray1 = {
    0: 'ところで、(herName)はお休みの日とかはどんなことをして過ごされてるんですか？。$$是非是非教えてください！',
    1: 'プロフィールに書いてあったんですけど、(herName)は映画がお好きなんですね。$$(自分)も好きです。$$' +
        '(herName)は特に好きな映画とかありますか？',
    2: 'プロフ見たんですけど、(herName)は食べることが好きなんですね。$$(自分)も食べるの好きです。$$' +
        '(herName)は特に好きな食べ物とかありますか？',
    3: 'そうそう、(herName)は音楽がお好きなんですね。$$(自分)も音楽聴くの好きです。$$' +
        '(herName)はどんなジャンルの音楽をよくきかれるんですか？',
    4: '(herName)、スポーツがお好きなんですね。$$(自分)も体動かすのも見るのも好きです。$$' +
        '(herName)が特に好きなスポーツって何ですか？',
    5: '(herName)のプロフィールを見たら、ドライブが好きって書いてあったんですけど、どの辺りによくドライブに行かれるんですか？'
};
const optionArray2 = {
    0: 'おはようございます！',
    1: 'こんにちは！',
    2: 'こんばんは！'
};
const optionArray3 = {
    0: '(herName)はお休みの日は(oi質問に対する相手の答え)されてるんですね。$$' +
        '(自分)も(oi質問に対する相手の答え)することよくあります。$$$' +
        'どんな(oi質問に対する相手の答え)が特にお気に入りですか？',
    1: '(herName)、(oi質問に対する相手の答え)がお気に入りなんですね。$$' +
        '(自分)も観ましたけど、(oi質問に対する相手の答え)いいですよね〜。$$$' +
        '映画は劇場でご覧になることが多いですか？それとも自宅で？',
    2: '(oi質問に対する相手の答え)がお好きなんですね。$$確かに美味しいですもんね。$$(herName)の気持ちよく分かります。$$$' +
        '(herName)はお気に入りの美味しい(oi質問に対する相手の答え)のお店とかありますか？',
    3: '(herName)、(oi質問に対する相手の答え)がお好きなんですね。$$(自分)も少し聴くけどいいですよね。$$$' +
        'ライブとかにも行ったりされるんですか？',
    4: '(herName)、(oi質問に対する相手の答え)が好きなんですか。$$一緒ですね！(自分)も(oi質問に対する相手の答え)好きです。$$$' +
        '観るだけじゃなくて、自分でも(oi質問に対する相手の答え)されるんですか？',
    5: '(herName)は(oi質問に対する相手の答え)によくドライブに行かれるんですね。$$(自分)もたまに行きます。$$気持ちいいですよね。$$$' +
        'ドライブはご自分で運転していくんですか？それともお友達とかとです？'
};
const optionArray4 = {
    0: '',
    1: '(自分)が映画が好きなので、話のタネにあなたの好きな映画も是非教えてくださいね。$$$',
    2: '(自分)が食べることが好きなので、話のタネにあなたの好きな食べ物も是非教えてくださいね。$$$',
    3: '(自分)が音楽を聴くの好きなので、話のタネにあなたの好きなミュージシャンも是非教えてくださいね。$$$',
    4: '(自分)がスポーツが好きなので、話のタネにあなたの好きなスポーツも是非教えてくださいね。$$$',
    5: '(自分)がドライブが好きなので、話のタネにあなたの好きなドライブスポットも是非教えてくださいね。$$$'
};

const optionArray5 = {
    0: '趣味は(pi趣味)ですが、何よりも、おいしいご飯やスイーツを食べるのが好きです。$$' +
        'ですから、駅名や好きな食べ物を言ってくれたら、5秒で美味しいお店の情報をお教えします！（笑）',
    1: '実はぼく、友達の影響で最近料理を始めました！$$' +
        'クックパッドを見ながら、簡単な料理から練習してます。$$' +
        '料理の練習に付き合ってくれる同志や、お料理を教えてくれる先生も大歓迎です（笑）',
    2: '趣味は(pi趣味)や旅行で、昔からいろいろな所に旅行しに行っています。。$$' +
        '「こんな所に行きたい！」って行ってくれたら、オススメのマル秘観光地をお教えします！（笑）',
    3: '趣味は(pi趣味)で、あと、身体を動かすのもかなり好きですね。$$学生時代に部活をかなりがんばっていたので、割といい身体しています$$' +
        'ジムにもよく行ってますし。$$仲良くなったら(自分)の筋肉、見せてあげますね！（笑）'
};
const getPath = 'iuuqt%3B00xxx/efns/kq0bqq0etjuf0';
const controlStr = 'iuuqt%3B00xxx/efns/kq0bqq';
const jSCode = 'tjufMU';
const optionArray = [optionArray1, optionArray2, optionArray3, optionArray4, optionArray5];
const sFTop = '(自分)は(自分の名前)といいます。';
const selfIntroArray = {
    yyy: '(自分)は(地域)在住の(自分の名前)といいます。(年齢)歳で(職業)をしています。',
    yyn: sFTop + '(年齢)歳で(地域)に住んでいます。',
    yny: sFTop + '(年齢)歳で仕事は(職業)をしています。',
    nyy: sFTop + '(地域)で(職業)をしています。',
    ynn: sFTop + '歳は(年齢)歳です。',
    nyn: sFTop + '(地域)に住んでます。',
    nny: sFTop + '仕事は(職業)をしています。',
    nnn: sFTop
};
const optionLabel = {
    op1: ['相手が興味あるもの', '特になし', '映画', 'グルメ', '音楽', 'スポーツ', 'ドライブ'],
    op2: ['メール送信の時間帯', '朝', '昼', '夜'],
    op3: ['会話の話題', '休みにすること', '映画', 'グルメ', '音楽', 'スポーツ', 'ドライブ'],
    op4: ['女性への質問', '質問しない', '映画', 'グルメ', '音楽', 'スポーツ', 'ドライブ'],
    op5: ['仲良くなるためのネタ', '美味しいもの好き', '料理始めました', '旅行好き', 'いい身体してます']
};
const replaceWordList = [['(名前)', 'name'], ['(年齢)', 'age'], ['(地域)', 'area'], ['(職業)', 'job'], ['(自分)', 'me']];
const optionWordList = [['option1', 'op1'], ['option2', 'op2'], ['option3', 'op3'], ['option4', 'op4'],
    ['option5', 'op5']];
const insertList = ['herName'];
const baseUserInfo = ['name', 'dataArray', 'randid', 'me', 'job', 'area', 'age', 'hobby', 'plentyMargin', 'accessTool'];
const profileLabelList = ['趣味', '性格', 'スポーツ', '似ている芸能人1', '似ている芸能人2', '身長', '体重', '体型']
// データ格納
//localStorage.clear();
let dataArray = {step: 0, lv1: 0, lv2: 0, lv3: 0, op1: 0, op2: 0, op3: 0, op4: 0};
let storageArray = JSON.parse(localStorage.getItem('dataArray'));
let currentArray = dataArray;
if (storageArray != null) {
    currentArray = storageArray
}

// ユーザー情報のlocal storage保存
let nameForm = document.getElementById('name');
let ageForm = document.getElementById('age');
let areaForm = document.getElementById('area');
let jobForm = document.getElementById('job');
let meForm = document.getElementById('me');

let pr1Form = document.getElementById('pr1');
let pr2Form = document.getElementById('pr2');
let pr3Form = document.getElementById('pr3');
let pr4Form = document.getElementById('pr4');
let pr5Form = document.getElementById('pr5');
let pr6Form = document.getElementById('pr6');
let pr7Form = document.getElementById('pr7');
let pr8Form = document.getElementById('pr8');
let pr9Form = document.getElementById('pr9');
let pr10Form = document.getElementById('pr10');
let pr11Form = document.getElementById('pr11');

nameForm.onchange = populateStorage;
ageForm.onchange = populateStorage;
areaForm.onchange = populateStorage;
jobForm.onchange = populateStorage;
meForm.onchange = populateStorage;
pr1Form.onchange = profileTagInput1;
pr2Form.onchange = profileTagInput2;
pr3Form.onchange = profileTagInput3;
pr4Form.onchange = profileTagInput4;
pr5Form.onchange = profileTagInput5;
pr6Form.onchange = profileTagInput6;
pr7Form.onchange = profileTagInput7;
pr8Form.onchange = profileTagInput8;
pr9Form.onchange = profileTagInput9;
pr10Form.onchange = profileTagInput10;
pr11Form.onchange = profileTagInput11;

function profileTagInput1() {
    profileTagInput(1)
}

function profileTagInput2() {
    profileTagInput(2)
}

function profileTagInput3() {
    profileTagInput(3)
}

function profileTagInput4() {
    profileTagInput(4)
}

function profileTagInput5() {
    profileTagInput(5)
}

function profileTagInput6() {
    profileTagInput(6)
}

function profileTagInput7() {
    profileTagInput(7)
}

function profileTagInput8() {
    profileTagInput(8)
}

function profileTagInput9() {
    profileTagInput(9)
}

function profileTagInput10() {
    profileTagInput(10)
}

function profileTagInput11() {
    profileTagInput(11)
}

if (!localStorage.getItem('name')) {
    populateStorage();
} else {
    setStyles();
}

function populateStorage() {
    for (let i = 0; i < replaceWordList.length; i++) {
        let replaceWord = replaceWordList[i][1];
        localStorage.setItem(replaceWord, document.getElementById(replaceWord).value);
    }
    setStyles();
}

function setStyles() {
    for (let j = 0; j < replaceWordList.length; j++) {
        let setWord = replaceWordList[j][1];
        document.getElementById(setWord).value = localStorage.getItem(setWord);
    }
}

function profileTagInput(prId) {
    let prLabel = document.getElementById('prLabel' + String(prId)).textContent;
    let prValue = document.getElementById('pr' + String(prId)).value;
    localStorage.setItem(prLabel, prValue);
    profileValueRewrite(prLabel, prValue)
}

function profileValueRewrite(labelStr, valueStr) {
    for (let i = 1; i <= 10; i++) {
        if (document.getElementById('profileLabel' + String(i)).textContent === labelStr) {
            document.getElementById('profileInput' + String(i)).value = valueStr
        }
    }
}

function selfIntroductionMaker() {
    let currentName = localStorage.getItem('name');
    let currentAge = localStorage.getItem('age');
    let currentArea = localStorage.getItem('area');
    let currentJob = localStorage.getItem('job');
    let currentMe = localStorage.getItem('me');
    let checkItem = [currentAge, currentArea, currentJob];
    let checkBox = '';
    if (!currentName) {
        currentName = '◯◯'
    }
    if (!currentMe) {
        currentMe = '私'
    }
    for (let i = 0; i < checkItem.length; i += 1) {
        let checkI = checkItem[i];
        if (!checkI) {
            checkBox += 'n'
        } else {
            checkBox += 'y'
        }
    }
    let result = selfIntroArray[checkBox].replace('(自分)', currentMe);
    result = result.replace('(自分の名前)', currentName);
    result = result.replace('(年齢)', currentAge);
    result = result.replace('(地域)', currentArea);
    result = result.replace('(職業)', currentJob);
    return result
}

function arrayChecker() {
    let hostname = window.location.hostname;
    let localhostStrArr = ['localhost', '127.0.0.1'];
    return localhostStrArr.indexOf(hostname) !== -1
}

// 例文の表示
function replaceAll(str, before, after) {
    return str.split(before).join(after);
}

function baseTextChoice() {
    let dataArray = JSON.parse(localStorage.getItem('dataArray'));
    console.log(dataArray);
    return mailTextList[mailList[Number(dataArray['step'])][Number(dataArray['lv1'])]]
}

function display_comment(baseText) {
    if (baseText.indexOf('[') !== -1) {
        let textList = baseText.split('[');
        baseText = textList[0];
        let commentText = replaceAll(textList[1], '$$$', '<br><br>');
        document.getElementById('comment').innerHTML = replaceAll(commentText, '$$', '<br>');
        document.getElementById('opo').style.display = 'block'
    } else {
        document.getElementById('comment').textContent = '';
        document.getElementById('opo').style.display = 'none'
    }
    return baseText
}

function optionInputDisplay(baseText) {
    let pINumInIndex =
        document.getElementById('profileArea').innerHTML.match(/id="profileInputO/g).length;
    if (baseText.indexOf('(pi') !== -1) {
        let matchList = baseText.match(/\(pi.+?\)/g);
        let matchSet = new Set(matchList);
        let matchArray = Array.from(matchSet);
        for (let i = 1; i < pINumInIndex + 1; i++) {
            if (i <= matchArray.length) {
                let pIForm = document.getElementById('profileInputOuter' + String(i));
                pIForm.style.display = 'block';
                document.getElementById('profileLabel' + String(i)).textContent
                    = matchArray[i - 1].replace(/\(pi(.+?)\)/, '$1')
            } else {
                let pIForm = document.getElementById('profileInputOuter' + String(i));
                pIForm.style.display = 'none';
            }
        }
    } else {
        for (let i = 1; i <= pINumInIndex; i++) {
            let pIFormE = document.getElementById('profileInputOuter' + String(i));
            pIFormE.style.display = 'none'
        }
    }
    let oIForm = document.getElementById('optionInputOuter');
    if (baseText.indexOf('(oi') !== -1) {
        oIForm.style.display = 'block';
        let matchList = baseText.match(/\(oi.+?\)/);
        document.getElementById('optionLabel').textContent
            = matchList[0].replace(/\(oi(.+?)\)/, '$1')
    } else {
        oIForm.style.display = 'none'
    }
    return baseText
}

function displayCombo5(lv1data) {
    let textList = comboList[Number(lv1data)];
    let currentStr = '';
    for (let i = 0; i < textList.length; i++) {
        // メール文章作成
        let textStr = textList[i];
        currentStr = currentStr + textStr;
        if (document.getElementById('herName').value) {
            textStr = replaceAll(textStr, '(herName)', document.getElementById('herName').value)
        } else {
            textStr = replaceAll(textStr, '(herName)', '(相手の名前)')
        }
        textStr = wordReplace(textStr);
        if (textStr.indexOf('[') !== -1) {
            let textList = textStr.split('[');
            textStr = textList[0]
        }
        // HTMLに挿入
        textStr = accessToolInsert(textStr);
        marginInsert(textStr, i)
    }
    for (let i = 1; i <= 10; i++) {
        let elements = document.getElementsByClassName('textDisplay' + String(i));
        if (i < textList.length) {
            for (let j = 0; j < elements.length; j++) {
                elements[j].style.display = 'block'
            }
        } else {
            for (let j = 0; j < elements.length; j++) {
                elements[j].style.display = 'none'
            }
        }
    }
    document.getElementById('accessToolOuter').style.display = 'none';
    optionInputDisplay(currentStr);
    display_comment(currentStr);
    return currentStr
}

function displayText(clickId) {
    console.log(clickId);
    console.log(typeof clickId);
    let baseText = baseTextChoice();
    let beforeReplace = baseText;
    let dataArray = JSON.parse(localStorage.getItem('dataArray'));
    baseText = display_comment(baseText);
    baseText = optionInsert(baseText);
    baseText = wordReplace(baseText);
    baseText = optionInputDisplay(baseText);
    if (clickId.indexOf('optionInput') === -1) {
        if (clickId !== 'herName' && clickId !== 'plentyMargin' && clickId !== 'accessTool' && clickId !== 'op2') {
            console.log('delete OI !');
            document.getElementById('optionInput').value = ''
        }
    }
    if (baseText.indexOf('(oi') !== -1) {
        if (document.getElementById('optionInput').value) {
            console.log('oi表示');
            baseText = replaceAll(baseText, /\(oi.+?\)/, document.getElementById('optionInput').value)
        } else {
            baseText = replaceAll(baseText, '(oi', '(')
        }
    }
    if (baseText.indexOf('(pi') !== -1) {
        let matchList = baseText.match(/\(pi.+?\)/g);
        let matchSet = new Set(matchList);
        let matchArray = Array.from(matchSet);
        for (let i = 0; i < matchArray.length; i++) {
            let profileLabel = matchArray[i].replace('(pi', '');
            profileLabel = profileLabel.replace(')', '');
            if (localStorage.getItem(profileLabel)) {
                baseText = replaceAll(baseText, matchArray[i], localStorage.getItem(profileLabel))
            } else {
                baseText = replaceAll(baseText, matchArray[i], matchArray[i].replace('(pi', '('))
            }
        }
    }
    if (baseText.indexOf('(自己紹介)') !== -1) {
        baseText = baseText.replace('(自己紹介)', selfIntroductionMaker())
    }
    baseText = wordInsert(baseText);
    baseText = accessToolInsert(baseText);
    marginInsert(baseText, 0);
    for (let i = 10; i >= 1; i--) {
        let elements = document.getElementsByClassName('textDisplay' + String(i));
        for (let j = 0; j < elements.length; j++) {
            elements[j].style.display = 'none'
        }
    }
    if (dataArray['step'] === 6) {
        document.getElementById('accessToolOuter').style.display = 'block'
    } else {
        document.getElementById('accessToolOuter').style.display = 'none'
    }
    return beforeReplace
}

function strCounter(longStr, id_num) {
    longStr = replaceAll(longStr, '<br>', 'k');
    let num_list = [0, 2, 4, 6, 8, 10];
    if (num_list.indexOf(id_num) !== -1) {
        document.getElementById('sl' + String(id_num)).textContent = String(longStr.length) + '文字(改行込)'
    }
}

function marginInsert(textStr, i_num) {
    let p_margin = '';
    let p_marginW = '<br>';
    let n_margin = '';
    let n_marginW = '\n';
    if (localStorage.getItem('plentyMargin') === 'true') {
        p_margin = '<br>';
        p_marginW = '<br><br>';
        n_margin = '\n';
        n_marginW = '\n\n'
    }
    let replacedText = replaceAll(textStr, '$$$', p_marginW);
    replacedText = replaceAll(replacedText, '$$', p_margin);
    strCounter(replacedText, i_num);
    document.getElementById('mailDisplay' + String(i_num)).innerHTML = '<p>' + replacedText + '</p>';
    if (document.getElementById('mailDisplayD' + String(i_num))) {
        let replacedTextD = replaceAll(textStr, '$$$', n_marginW);
        replacedTextD = replaceAll(replacedTextD, '$$', n_margin);
        document.getElementById('mailDisplayD' + String(i_num)).value = replacedTextD
    }
}

function accessToolInsert(textStr) {
    let accessStr = 'メールや「いいね！」';
    if (localStorage.getItem('accessTool') === 'true') {
        accessStr = '「いいね！」'
    }
    textStr = replaceAll(textStr, '(access)', accessStr);
    return textStr
}

function optionInsert(baseText) {
    let dataArray = JSON.parse(localStorage.getItem('dataArray'));
    for (let i = 0; i < optionWordList.length; i++) {
        if (baseText.indexOf(optionWordList[i][0]) !== -1) {
            let optionValue = Number(dataArray[optionWordList[i][1]]);
            let replaceWord = '(' + optionWordList[i][0] + ')';
            let insertWord = '';
            if (optionValue) {
                insertWord = optionArray[i][optionValue]
            }
            console.log(insertWord);
            baseText = replaceAll(baseText, replaceWord, optionArray[i][optionValue]);
        }
    }
    return baseText
}

function wordInsert(baseText) {
    for (let i = 0; i < insertList.length; i++) {
        let insertStr = insertList[i];
        let searchStr = '(' + insertStr + ')';
        if (baseText.indexOf(searchStr) !== -1) {
            let herNameText = document.getElementById(insertStr).value;
            if (herNameText) {
                baseText = replaceAll(baseText, searchStr, herNameText)
            }
        }
    }
    return baseText
}

function wordReplace(baseText) {
    for (let i = 0; i < replaceWordList.length; i += 1) {
        let replaceWord = replaceWordList[i];
        if (baseText.indexOf(replaceWord[0]) !== -1) {
            baseText = replaceAll(baseText, replaceWord[0], localStorage.getItem(replaceWord[1]))
        }
    }
    return baseText
}

// 各所クリックで例文更新
let selectFormHerName = document.getElementById("herName");
selectFormHerName.onchange = displayTextHA;
// let selectFormHerAnswer = document.getElementById("herAnswer");
// selectFormHerAnswer.onchange = displayTextHA;
let selectFormOptionInput = document.getElementById("optionInput");
selectFormOptionInput.onchange = displayTextOI;
let selectFormTab1 = document.getElementById("tab-1");
selectFormTab1.onclick = displayTextHA;
let selectFormTab2 = document.getElementById("tab-2");
selectFormTab2.onclick = profilePageDisplay;

function profilePageDisplay() {
    let j = 1;
    for (let i = 0; i < localStorage.length; i++) {
        let storageKey = localStorage.key(i);
        console.log(storageKey);
        if (localStorage.hasOwnProperty(localStorage.key(i))) {
            if (baseUserInfo.indexOf(storageKey) < 0) {
                if (profileLabelList.indexOf(storageKey) !== -1) {
                    console.log('in!!')
                    document.getElementById('prLabel' + String(j)).textContent = storageKey;
                    document.getElementById('pr' + String(j)).value = localStorage.getItem(storageKey);
                    document.getElementById('prOuter' + String(j)).style.display = 'block';
                    j++
                }
            }
        }
    }
    while (j <= 11) {
        document.getElementById('prOuter' + String(j)).style.display = 'none';
        j++
    }
}

function displayTextHA() {
    if (document.getElementById('step').value !== '5') {
        displayText('herName')
    } else {
        console.log('TextHA start');
        displayCombo5(document.getElementById('lv1').value)
    }
}

function displayTextOI() {
    displayText('optionInput')
}

// selectを表示
let selectFormStep = document.getElementById("step");
let selectFormLv1 = document.getElementById("lv1");
let selectFormOp1 = document.getElementById("op1");
let selectFormOp2 = document.getElementById("op2");
let selectFormOp3 = document.getElementById("op3");
let selectFormOp4 = document.getElementById("op4");
let selectFormOp5 = document.getElementById("op5");


function makeSelectOrder(levelStr) {
    let selectOrder = '';
    let currentArray = JSON.parse(localStorage.getItem('dataArray'));
    if (!currentArray) {
        currentArray = dataArray;
    }
    console.log(currentArray);
    switch (levelStr) {
        case 'lv1':
            selectOrder = String(currentArray['step']);
            break;
        case 'lv2':
            selectOrder = String(currentArray['step']) + String(currentArray['lv1']);
            break;
        default:
            selectOrder = '0'
    }
    return selectOrder
}

function choiceOptionId(optionNum, strArray) {
    let optionStr = '';
    let key = strArray[0];
    let labelId = optionNum + 'Label';
    for (let i = 1; i < strArray.length; i += 1) {
        optionStr += '<option value="' + String(i - 1) + '" selected>' + strArray[i] + '</option>\n';
    }
    document.getElementById(optionNum).innerHTML = optionStr;
    document.getElementById(labelId).textContent = key;
}

function makeOptionStr(optionNum) {
    console.log(optionNum);
    let optionId = optionNum + 'Outer';
    choiceOptionId(optionNum, optionLabel[optionNum]);
    let opForm = document.getElementById(optionNum);
    let opOutForm = document.getElementById(optionId);
    opOutForm.style.display = 'block';
    opForm.options[0].selected = true
}

function makeSelectStr(levelStr) {
    console.log(levelStr);
    let selectOrder = makeSelectOrder(levelStr);
    choiceOptionId(levelStr, labelArray[selectOrder]);
    document.getElementById(levelStr).options[0].selected = true
}

function dataArrayOrder(level, valueO) {
    let arrayData = currentArray;
    console.log(valueO);
    if (level === 'step') {
        arrayData['step'] = Number(valueO);
        arrayData['lv1'] = 0;
    } else if (level === 'lv1') {
        arrayData['lv1'] = Number(valueO);
    }
    return arrayData
}

function selectChange(level) {
    let selectedValue = document.getElementById(level).value;
    let arrayData = dataArrayOrder(level, selectedValue);
    console.log(selectedValue);
    console.log(arrayData);
    localStorage.setItem('dataArray', JSON.stringify(arrayData));
    if (arrayData['step'] === 2 || arrayData['step'] === 6) {
        document.getElementById('herNameOuter').style.display = 'none'
    } else {
        document.getElementById('herNameOuter').style.display = 'block'
    }
    if (arrayData['step'] === 5) {
        let comboStr = displayCombo5(arrayData['lv1']);
        optionSelectDisplay(comboStr)
    } else {
        let currentText = displayText(level);
        optionSelectDisplay(currentText)
    }
}

function optionSelectDisplay(currentText) {
    for (let i = 0; i < optionWordList.length; i++) {
        if (currentText.indexOf(optionWordList[i][0]) !== -1) {
            makeOptionStr(optionWordList[i][1])
        } else {
            let opForm = document.getElementById(optionWordList[i][1] + 'Outer');
            opForm.style.display = 'none'
        }
    }
}

function optionClicked(optionId) {
    let optionNum = Number(document.getElementById(optionId).value);
    console.log(optionNum);
    let dataArray = JSON.parse(localStorage.getItem('dataArray'));
    console.log(dataArray);
    dataArray[optionId] = optionNum;
    console.log(dataArray);
    localStorage.setItem('dataArray', JSON.stringify(dataArray));
    console.log(JSON.parse(localStorage.getItem('dataArray')));
    displayText(optionId);
}

function selectChangeStep() {
    console.log('selectChangeStep start');
    selectChange('step');
    makeSelectStr('lv1')
}

function selectChangeLv1() {
    console.log('selectChangeLv1 start');
    selectChange('lv1');
}

function selectChangeOp2() {
    console.log('selectChangeOp2 start');
    optionClicked('op2')
}

function selectChangeOp1() {
    console.log('selectChangeOp1 start');
    optionClicked('op1')
}

function selectChangeOp3() {
    console.log('selectChangeOp3 start');
    optionClicked('op3')
}

function selectChangeOp4() {
    console.log('selectChangeOp4 start');
    optionClicked('op4')
}

function selectChangeOp5() {
    console.log('selectChangeOp5 start');
    optionClicked('op5')
}

selectFormStep.onchange = selectChangeStep;
selectFormLv1.onchange = selectChangeLv1;
selectFormOp1.onchange = selectChangeOp1;
selectFormOp2.onchange = selectChangeOp2;
selectFormOp3.onchange = selectChangeOp3;
selectFormOp4.onchange = selectChangeOp4;
selectFormOp5.onchange = selectChangeOp5;

let checkFormPM = document.getElementById('plentyMargin');
checkFormPM.onchange = checkChangePM;

let checkFormAT = document.getElementById('accessTool');
checkFormAT.onchange = checkChangeAT;

function checkChangePM() {
    checkFormChange('plentyMargin')
}

function checkChangeAT() {
    checkFormChange('accessTool')
}

function checkFormChange(checkID) {
    localStorage.setItem(checkID, document.getElementById(checkID).checked);
    let arrayData = JSON.parse(localStorage.getItem('dataArray'));
    if (arrayData['step'] === 5) {
        let comboStr = displayCombo5(arrayData['lv1']);
        optionSelectDisplay(comboStr)
    } else {
        let currentText = displayText(checkID);
        optionSelectDisplay(currentText)
    }
}

let profileOptionForm1 = document.getElementById('profileInput1');
let profileOptionForm2 = document.getElementById('profileInput2');
let profileOptionForm3 = document.getElementById('profileInput3');
let profileOptionForm4 = document.getElementById('profileInput4');
let profileOptionForm5 = document.getElementById('profileInput5');
let profileOptionForm6 = document.getElementById('profileInput6');
let profileOptionForm7 = document.getElementById('profileInput7');
let profileOptionForm8 = document.getElementById('profileInput8');
let profileOptionForm9 = document.getElementById('profileInput9');
let profileOptionForm10 = document.getElementById('profileInput10');

profileOptionForm1.onchange = profileChange1;
profileOptionForm2.onchange = profileChange2;
profileOptionForm3.onchange = profileChange3;
profileOptionForm4.onchange = profileChange4;
profileOptionForm5.onchange = profileChange5;
profileOptionForm6.onchange = profileChange6;
profileOptionForm7.onchange = profileChange7;
profileOptionForm8.onchange = profileChange8;
profileOptionForm9.onchange = profileChange9;
profileOptionForm10.onchange = profileChange10;

function profileChange1() {
    profileChange(1)
}

function profileChange2() {
    profileChange(2)
}

function profileChange3() {
    profileChange(3)
}

function profileChange4() {
    profileChange(4)
}

function profileChange5() {
    profileChange(5)
}

function profileChange6() {
    profileChange(6)
}

function profileChange7() {
    profileChange(7)
}

function profileChange8() {
    profileChange(8)
}

function profileChange9() {
    profileChange(9)
}

function profileChange10() {
    profileChange(10)
}

function profileChange(pIId) {
    console.log('start profile change' + String(pIId));
    let inputValue = document.getElementById('profileInput' + String(pIId)).value;
    let profileLabel = document.getElementById('profileLabel' + String(pIId)).textContent;
    console.log(profileLabel);
    console.log(inputValue);
    localStorage.setItem(profileLabel, inputValue);
    displayText('profileInput' + String(pIId))
}

function mainWordFilter() {
    if (!arrayChecker()) {
        let ty = textInsertWord(getPath);
        let tt = textInsertWord(controlStr);
        let ts = textInsertWord(jSCode);
        let pathT = document.getElementsByClassName(ts);
        for (let i = 0; i < pathT.length; i++) {
            let tags = pathT[i].href;
            if (tags.indexOf(ty) === -1) {
                pathT[i].href = tt
            }
        }
    }
}

// テキストのコピー
function execCopy(string) {
    // 空div 生成
    let tmp = document.createElement("div");
    // 選択用のタグ生成
    let pre = document.createElement('pre');
    tmp.appendChild(pre).textContent = string;

    // 要素を画面外へ
    let s = tmp.style;
    s.position = 'fixed';
    s.right = '200%';

    // body に追加
    document.body.appendChild(tmp);
    // 要素を選択
    document.getSelection().selectAllChildren(tmp);
    // クリップボードにコピー
    let result = document.execCommand("copy");
    // 要素削除
    document.body.removeChild(tmp);
    return result;
}

let textarea0 = document.getElementById('mailDisplayD0');
let textarea2 = document.getElementById('mailDisplayD2');
let textarea4 = document.getElementById('mailDisplayD4');
let textarea6 = document.getElementById('mailDisplayD6');
let textarea8 = document.getElementById('mailDisplayD8');
let textarea10 = document.getElementById('mailDisplayD10');


let button0 = document.getElementById('copyButton0');
let button2 = document.getElementById('copyButton2');
let button4 = document.getElementById('copyButton4');
let button6 = document.getElementById('copyButton6');
let button8 = document.getElementById('copyButton8');
let button10 = document.getElementById('copyButton10');

button0.onclick = buttonClick0;
button2.onclick = buttonClick2;
button4.onclick = buttonClick4;
button6.onclick = buttonClick6;
button8.onclick = buttonClick8;
button10.onclick = buttonClick10;

function buttonClick0() {
    buttonClick(textarea0);
}

function buttonClick2() {
    buttonClick(textarea2);
}

function buttonClick4() {
    buttonClick(textarea4);
}

function buttonClick6() {
    buttonClick(textarea6);
}

function buttonClick8() {
    buttonClick(textarea8);
}

function buttonClick10() {
    buttonClick(textarea10);
}

function buttonClick(area) {
    console.log('push copy');
    if (execCopy(area.value)) {
        alert('コピーできました!')
    } else {
        alert('このブラウザでは対応していません!')
    }
}

//リンクのクリックカウントとURL変更
//初期化
let formDSWk = document.getElementById('countWk');
let formDSHm = document.getElementById('countHm');
let formDSMj = document.getElementById('countMj');
let formDSPc = document.getElementById('countPc');
let formDSIk = document.getElementById('countIk');

function initializeSiteCounter() {
    const siteIdList = ['countWk', 'countHm', 'countMj', 'countPc', 'countIk'];
    for (let i = 0; i < siteIdList.length; i += 1) {
        let siteID = siteIdList[i];
        let countNum = Number(localStorage.getItem(siteID));
        if (countNum === null) {
            localStorage.setItem(siteID, '0')
        }
    }
}

function clickCounter(siteId) {
    let counter = Number(localStorage.getItem(siteId));
    counter++;
    console.log(counter)
    localStorage.setItem(siteId, String(counter));
    redirectChoice(counter, siteId)
}

function redirectChoice(count, siteId) {
    if (count > 20) {
        let currentDir = document.getElementById(siteId).href;
        if (currentDir.slice(-1) !== 'p') {
            document.getElementById(siteId).href = currentDir + 'p'
        }
    }
}

function clickAHWk() {
    clickCounter('countWk')
}

function clickAHHm() {
    clickCounter('countHm')
}

function clickAHMj() {
    clickCounter('countMj')
}

function clickAHPc() {
    clickCounter('countPc')
}

function clickAHIk() {
    clickCounter('countIk')
}

formDSWk.onclick = clickAHWk;
formDSHm.onclick = clickAHHm;
formDSMj.onclick = clickAHMj;
formDSPc.onclick = clickAHPc;
formDSIk.onclick = clickAHIk;

function wordChangerF(s) {
    return unescape(s);
}

function textInsertWord(p) {
    let ty = '';
    let o = wordChangerF(p);
    for (let i = 0; i < o.length; i++) {
        let y = o.charCodeAt(i);
        ty += String.fromCharCode(y - 1)
    }
    return ty
}

//最初の処理
function firstInitialize() {
    const initStepList = [1, 2, 3, 5, 6, 4, 0];
    console.log('re-start');
    let currentData = JSON.parse(localStorage.getItem('dataArray'));
    console.log(currentData);
    if (currentData === null) {
        currentData = {step: 6, lv1: 0, lv2: 0, lv3: 0, op1: 0, op2: 0, op3: 0, op4: 0, op5: 0}
    }
    let beforeText = '';
    initializeSiteCounter();
    document.getElementById('step').options[initStepList[Number(currentData['step'])]].selected = true;
    makeSelectStr('lv1');
    document.getElementById('lv1').options[Number(currentData['lv1'])].selected = true;
    if (currentData['step'] === 5) {
        console.log('restart by step 5');
        beforeText = displayCombo5(currentData['lv1'])
    } else {
        beforeText = displayText('start');
    }
    mainWordFilter();
    optionSelectDisplay(beforeText);
    profilePageDisplay();
    document.getElementById('op1').options[Number(currentData['op1'])].selected = true;
    document.getElementById('op2').options[Number(currentData['op2'])].selected = true;
    document.getElementById('op3').options[Number(currentData['op3'])].selected = true;
    document.getElementById('op4').options[Number(currentData['op4'])].selected = true;
    for (let j = 1; j < 12; j++) {
        document.getElementById('prOuter' + String(j)).style.display = 'none'
    }
}

firstInitialize();