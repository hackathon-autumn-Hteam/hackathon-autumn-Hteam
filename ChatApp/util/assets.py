from flask_assets import Environment, Bundle


def bundle_css_files(app):
    # CSSファイルのバンドル（圧縮・結合）
    assets = Environment(app)

    #  CSSファイルをまとめて1つのファイルに結合し、さらに圧縮する設定を定義
    # - 'css/*.css'：対象となるCSSファイル。cssフォルダ配下のすべてのCSSが対象
    # - filters='cssmin'：圧縮（最小化）フィルターを適用。空白や改行などを削除してファイルサイズを削減
    # - output='gen/bundled.css'：出力先。まとめられたCSSは gen フォルダに bundled.css という名前で生成される
    css_bundle = Bundle("css/*.css", filters="cssmin", output="gen/bundled.css")
    assets.register("css_all", css_bundle)
    css_bundle.build()
