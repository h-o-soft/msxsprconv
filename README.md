# MSX Sprite Converter

# 概要
msxsprconvは、8x8または16x16サイズの画像をMSXのスプライトデータに変換するコンバートツールです。

基本的にMSX(1)のみの対応で、複数色を使った画像については、色数ぶんの画像に分離した状態で出力します(例えば、3色を使うと、3枚の画像を出力します)。

出力フォーマットはテキスト(アセンブラソース)と、バイナリの二種類を選択可能となっています。

# 必要なもの

* Python3
* Pillow
* argparse

# 使い方

```
MSX Sprite Converter Version 0.2.0 Copyright 2022 H.O SOFT Inc.

positional arguments:
  path                  image path

optional arguments:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  Sprite Size ( 8 or 16 ) [default = 16]
  -l LABEL, --label LABEL
                        Assembler Label [default = "_sprite"]
  -o OUTPUT, --output OUTPUT
                        Directs the output to a name of your choice
  -f {txt,bin}, --format {txt,bin}
                        Output format text or binary [default= "txt"]
  -c, --comment         Add long information comment (only txt format)
```

$ msxsprconv.py grp.png

画像ファイルを引数に指定すると、テキスト(アセンブラ)形式に変換したものを標準出力に出力します。
オプションとして「-s 8」をつけると8x8のスプライト、「-s 16」をつけると、16x16のスプライトとして変換します。
出力の順番は、下記のとおりです。

* 16x16フォーマットで横に2つ並べた場合(32x16)
```
1 3 5 7
2 4 6 8
```

数字1つが8x8のスプライト画像情報で、それが4つ集まって16x16の画像1つを表現します。
上記の場合「1、2、3、4」で1つ目、「5、6、7、8」で2つ目のスプライト画像を構成します。
この順番でVRAMに転送する事で、MSXは16x16のスプライトを表示出来ます。

* 8x8フォーマットで横に2つ、縦に2つ並べた場合(16x16)
```
1 2
3 4
```

8x8の場合は素直に8x8の画像を横に拾っていき、右端まで行ったら左下に移動して繰り返して変換します。

## 複数色を使ったスプライト画像の変換

複数色を使っていた場合、使った色数ぶんの単色画像に分離した状態で、スプライトデータを作ります。
また、複数色を使った場合、MSX(1)のパレット番号の若い順に出力されます。
出力される順番は下記のとおりです。

* 16x16の複数色スプライトの場合

```
16x16の1つ目の1色目(8x8を4個ぶん)
16x16の1つ目の2色目(同上)
16x16の2つ目の1色目(同上)
16x16の2つ目の2色目(同上)
...
(以下繰り返し)
```

* 8x8の複数色スプライトの場合

```
1つ目の1色目
1つ目の2色目
2つ目の1色目
2つ目の2色目
...
(以下繰り返し)
```

## コメント情報について

テキスト出力した場合、下記のようなコメントがつきます。

### 16x16の場合のコメント

```
        DB $00,$00,$00,$00,$03,$05,$05,$03 ; 0,0 9
        DB $00,$00,$00,$18,$00,$06,$03,$01 ; 0,0 9
        DB $00,$00,$00,$00,$c0,$60,$60,$c0 ; 0,0 9
        DB $00,$00,$08,$00,$00,$30,$38,$18 ; 0,0 9
        DB $07,$08,$07,$00,$40,$70,$70,$38 ; 0,0 15
        DB $0c,$0e,$1f,$07,$07,$01,$00,$00 ; 0,0 15
        DB $e0,$10,$e0,$00,$02,$0e,$0e,$0e ; 0,0 15
        DB $0c,$d0,$a0,$5e,$fc,$c0,$00,$00 ; 0,0 15
        DB $00,$00,$00,$00,$00,$03,$05,$05 ; 1,0 9
        DB $03,$00,$00,$18,$00,$00,$06,$01 ; 1,0 9
        DB $00,$00,$00,$00,$00,$c0,$60,$60 ; 1,0 9
        DB $c0,$00,$08,$00,$00,$00,$38,$18 ; 1,0 9
        DB $00,$07,$08,$07,$00,$00,$00,$00 ; 1,0 15
        DB $08,$1c,$3e,$27,$67,$47,$01,$00 ; 1,0 15
        DB $00,$e0,$10,$e0,$00,$00,$00,$00 ; 1,0 15
        DB $08,$0e,$d6,$af,$5f,$fd,$c0,$00 ; 1,0 15
```

「0,0 9」は「画像を16x16に分離した場合の0,0(x,y)の位置にある色番号9番」といった意味となります。
「0,0 15」は、同じ位置にある色番号15(白)の画像データで、「1,0 9」は、二つ目の画像の色番号9の画像、「1,0 15「は二つ目の画像の色番号15の画像、という事になります。

行ごとにコメントをつけたくない場合は「-c」オプションをつける事で、下記のようなコメントになります。

```
 ; 0,0 COL 9 : (255,137,125)
        DB $00,$00,$00,$00,$03,$05,$05,$03
        DB $00,$00,$00,$18,$00,$06,$03,$01
        DB $00,$00,$00,$00,$c0,$60,$60,$c0
        DB $00,$00,$08,$00,$00,$30,$38,$18
; 0,0 COL 15 : (255,255,255)
        DB $07,$08,$07,$00,$40,$70,$70,$38
(略)
```

-cをつけない場合とほぼ同様ですが、色コードが追加されます。

### 8x8の場合のコメント

通常は下記のようになります。16x16とあまり変わりません。

```
        DB $00,$00,$00,$00,$03,$05,$05,$03 ; 0,0 9
        DB $07,$08,$07,$00,$40,$70,$70,$38 ; 0,0 15
        DB $00,$00,$00,$00,$c0,$60,$60,$c0 ; 1,0 9
        DB $e0,$10,$e0,$00,$02,$0e,$0e,$0e ; 1,0 15
```

「-c」をつけると下記のようになります。冗長なので、あまり使う事はないでしょう。

```
; 0,0 COL 9 : (255,137,125)
        DB $00,$00,$00,$00,$03,$05,$05,$03
; 0,0 COL 15 : (255,255,255)
        DB $07,$08,$07,$00,$40,$70,$70,$38
; 1,0 COL 9 : (255,137,125)
        DB $00,$00,$00,$00,$c0,$60,$60,$c0
; 1,0 COL 15 : (255,255,255)
        DB $e0,$10,$e0,$00,$02,$0e,$0e,$0e
```

### 出力ファイルの指定

オプションとして「-o ファイルネーム」をつけると、ファイルネームで指定したファイルにデータを出力します。
この場合、標準出力には何も出力されません。

### バイナリモード

オプションとして「-f bin」をつけると、バイナリデータを出力します。
データの並びは変わらず、コメントなどはもちろん無い状態で素のバイナリが出力されますので、ROMへそのまま埋め込むなど、適宜自由にお使いください。

また、出力ファイルを指定する「-o」オプションをつけない場合、標準出力にバイナリを出力しますので、ご注意ください。

## 色

msxsprconvはMSX(1)用なので、下記のMSX(1)パレットの色を使った画像のみを扱えます。
画像の透明部分は0番の色として扱われ、それ以外の色は、下記の色に一番近い色が選択されます。必ずしも色が完全に一致している必要はありませんが、それなりに正しい色で表示するためには、下記の色を使って画像を作成すると良いでしょう。

| Num | Color|
| ------------- | ------------- |
| 0 | ![](https://via.placeholder.com/16/000000/FFFFFF/?text=%20) `#000000` |
| 1 | ![](https://via.placeholder.com/16/000000/FFFFFF/?text=%20) `#000000` |
| 2 | ![](https://via.placeholder.com/16/3eb849/FFFFFF/?text=%20) `#3eb849` |
| 3 | ![](https://via.placeholder.com/16/74d07d/FFFFFF/?text=%20) `#74d07d` |
| 4 | ![](https://via.placeholder.com/16/5955e0/FFFFFF/?text=%20) `#5955e0` |
| 5 | ![](https://via.placeholder.com/16/8076f1/FFFFFF/?text=%20) `#8076f1` |
| 6 | ![](https://via.placeholder.com/16/b95e51/FFFFFF/?text=%20) `#b95e51` |
| 7 | ![](https://via.placeholder.com/16/65dbef/FFFFFF/?text=%20) `#65dbef` |
| 8 | ![](https://via.placeholder.com/16/db6559/FFFFFF/?text=%20) `#db6559` |
| 9 | ![](https://via.placeholder.com/16/ff897d/FFFFFF/?text=%20) `#ff897d` |
|10 | ![](https://via.placeholder.com/16/ccc35e/FFFFFF/?text=%20) `#ccc35e` |
|11 | ![](https://via.placeholder.com/16/ded087/FFFFFF/?text=%20) `#ded087` |
|12 | ![](https://via.placeholder.com/16/3aa241/FFFFFF/?text=%20) `#3aa241` |
|13 | ![](https://via.placeholder.com/16/b766b5/FFFFFF/?text=%20) `#b766b5` |
|14 | ![](https://via.placeholder.com/16/cccccc/FFFFFF/?text=%20) `#cccccc` |
|15 | ![](https://via.placeholder.com/16/ffffff/FFFFFF/?text=%20) `#ffffff` |
