# ahc045

1. 場所を推定する  
とりあえず範囲の中心とする（占いは後）
1. 辺を作る  
ざっくり範囲を区切って順番に使う


位置が推定できたと仮定した場合
1. グループ分けを適当に決めてから焼く
   1. 適当に１つ取って、近めの別グループを見つけてスワップ

相対位置しか分からないから推定できないのでは？

占って分かるのはどのような情報？
1. それぞれが比較的近い点が分かる　ある点から見た距離順
2. ABCならAB,BC,CAでどれが一番長いか分かる　→　その中ではベストな配置
3. 使わない方がいい辺を見つけていくことになる？


Lが小さいと、占わずに中心位置で作った時とほとんど変わっていなかったので、もっと有効な使い方をしないといけなさそう

Wが小さい時も、占いなしと差を出せていない

位置が不明確な都市を優先的に占う
1. 近くにある想定だったものが本当に近くにあるのか？に注目する

都市ごとに誤差が異なっていて、W=2500だったとしても、800都市のうち16都市くらいは
2500/50=50くらいの誤差になる

重複分をスキップするだけでなく、同じ優先度で採用されなかったものを占う

改善しどころ
1. そこそこ近くて違うグループになった都市
2. 誤差が大きい都市から出す道

そもそもグループサイズの分布はどうなる？
僻地を次数２にしたくないが対応は難しそう。
占いへの渡し方は中心推定ベースでいいのか？
推定が合っているならそもそも占う必要がないため、間違っていそうなところを占いたい。
これはすでに多少やっている。
誤差が大きい都市や次数が高い都市からやっていきたい

得られる情報量が大きくなるように占いをしたい

占いが余っていたら、近くの別グループを一緒に入れて、次数１にならなかったら入れ替えた方がいいかも
大きい木を作ってから分割した方がいいかも？

だんだん辺を増やしていく方式？

グループサイズ15までで、全体の都市の半分くらいをカバーしている
推定値で近い都市３つ出すとどのくらい当たる？

最適とどのくらい辺が違うか？
半分くらい合ってる？
