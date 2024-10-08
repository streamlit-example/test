

## MVPパターン
### はじめに
- アーキテクチャ論は議論のコンテキストによって前提が異なることがあり、それによって解釈に幅が生じている
- 本来ならば原典から解釈していくべきだが、今回は厳密性にそこまで工数をかけるべきでないと判断し、Web上の情報の最大公約数をとるにとどめた。

### 概要
- アプリケーションのソースコードを以下3つのコンポーネントに分割する設計思想。
    - Model
    - View
    - Presenter
- ポイントは各コンポーネントに関心を分離させること。（＝疎結合にすること）
- 関心の分離が上手くできた場合のメリットは以下。
    - **高可読性**
        - 依存関係が明らかで、全体構成の把握やメンテ対象個所の特定が容易
        - バグの発生抑制、発見時間短縮に有効
        - 「車輪の再開発」の防止にも有効
    - **テスト容易性**
        - コンポーネントごとに単体テストを実行しやすい
        - Viewのテストが困難な場合もPresenterのロジックに対するテストは容易
        - デグレ防止、開発スピード向上に有効
    - **柔軟性**
        - 改修が他コンポーネントに影響しにくい
    - **再利用性**
        - View/Modelの技術を変更しても他のコンポーネントはコードを再利用できる
- デメリットは以下。
    - 責任の分離をしすぎるとソースコード量が増えるので開発コストが高くなってしまう。
    - モック作成初期など、頻繁に大幅な変更が加わる段階では適さない。
        - [MVP (Model-View-Presenter)](https://www.querier.io/ja/glossary/mvp)

### 各コンポーネントの特徴
- **Model**
    - 役割: バックエンド。データ操作、ビジネスロジックの定義、外部APIの操作
    - PresenterやViewのコードがなくとも業務要件が読み取れる
- **View**
    - 役割: UI。ユーザへの情報の表示とインプットの受け取り
    - Viewのコードがあれば画面の表示内容と画面から入力できる内容が明らかである
- **Presenter**
    - 役割: ModelとViewの仲介/取り纏め/制御。表示における条件分岐なども担当
    - フロントエンド側に配置する
    - 仕様書となる（これを読めば処理の流れが分かる）


### 本プロジェクトにおけるアーキ案
考慮すべきと思われる要素は以下。
- Streamlitとの併用
    - Streamlitはコンパクトなコードを一か所に集中させるスタイルを想定している
    - ViewとPresenterを分離させようとするとコード量が増加する可能性がある
- Azureの利用
    - MVPパターン採用に関わらずバックエンドは分離する予定であった。
    - マイクロサービス化に関しても特に影響はない

上記を踏まえ、各コンポーネントの関心の範囲や実装上のルールを以下のように定める。

- **model**
    - ファイル/クラスは機能単位で分割する
    - データ操作(CRUD)
    - ビジネスロジックの定義
    - 外部APIの操作の定義
    - 上記捜査に密接にかかわる通知文言の定義
    - 利用するライブラリ: `pd`, `np`, `fastapi`, `requests`, ...
        - `st`や`stss`はインポートしない
    - コード内でViewやPresenterを利用しない
    - マイクロサービス化する場合、対象はmodelのみ
- **view**
    - ファイル: メイン + 各タブ + サイドバー
    - クラス: メイン + 各タブ + 各ダイアログボックス + サイドバー
    - 画面表示の定義
    - インプットの受け取り処理の定義
    - `__init__`（コンストラクタ）: レイアウトと静的コンテンツを定義する
    - `input`: ボタン等によるユーザコマンドを受け取る（`controller` と呼んでもいいかも）
    - `table`: 表を表示し、ユーザによる操作の受け取る
    - 利用するライブラリ: `st`, `plt` のみ(現状)
    - コード内でModelやPresenterを利用しない
- **presenter**
    - ファイル: メイン + 各タブ + サイドバー
    - クラス: ファイルと一対一で定義
    - アプリケーションの処理フローの定義
    - 表示における条件分岐(編集モードの切り替えなど)
    - 入力バリデーション
    - 利用するライブラリ: `st.session_state`, `st.rerun`, `st.dialog`
        - `st`はインポートしない
    - 主に `Presenter.state` において、辞書型でセッション状態を保持する
    - UI要素のリフレッシュのために、`Presenter.key_number` `Presenter.count_up()` を利用する
        - 上記以外は状態として保持しない
        - ※データは適宜`st.cache`でキャッシュする
    - コード内でModelやPresenterのメソッドを利用する
- **apps**: 各アプリのエントリーポイント
- **utils**: 便利ツール
    - **page_manager**
        - 簡単にマルチページ化するためのツール
    - データ整形
- **tests**: テストコード


### 他のパターン
- MVC（Model-View-Controller）
    - ControllerがViewの更新を行う。
    - テレビゲームのようにVとCが分離する場合と、通常のWebアプリのようにVとCが不可分の場合がある。
    - 前者では責任の分離がしやすそう（※深く考えてない）
        - [モデル・ビュー・プレゼンタ](https://zenn.dev/twugo/books/21cb3a6515e7b8/viewer/57bd76)
    - 一方、後者では「Model-ViewController」という2コンポーネントでの整理をされているらしく、多機能のViewControllerが問題になることが多いようである
        - [節子、それViewControllerやない...、FatViewControllerや...。](https://www.slideshare.net/slideshow/viewcontrollerfatviewcontroller-79796852/79796852)
- MVVM（Model-View-ViewModel）
    - ViewModelが双方向データバインディングを使用してViewを更新する
    - 難易度高め
- クリーンアーキテクチャ
    - 全然理解できてないがアンチが多い
    - 原典とかなり異なりそうな話がWeb上に多くある
    - [クリーンアーキテクチャの功罪](https://zenn.dev/adwd/articles/5d4a89262f4fc5)



## 図
まず、Model以外のコンポーネントの構成と依存関係を以下に示す。
- `main.py`, `apps`は多少簡略化して書いている。
- この図は`app1.py`に関する依存関係を示す。
- `home.py`, `app2.py`は未実装であり、下図では割愛する。`app1.py`と類似の依存関係を今後実装する見込み。
- Presenterのフォルダはアプリごとに分けてもよいかもしれない。

```mermaid
graph LR;


Presenter --> View;
SidebarPresenter --> SidebarView;
PartsPresenter --> PartsView;
PartsPresenter --> PartsXxxView;
RegisterPresenter --> RegisterView;
RegisterPresenter --> RegisterConfirmView;
FilePresenter --> FileView;
FilePresenter --> FileXxxView;

main.py --> app1.py;
app1.py --> Presenter;
Presenter --> SidebarPresenter;
Presenter --> PartsPresenter;
Presenter --> RegisterPresenter;
Presenter --> FilePresenter;

subgraph apps;
    home.py;
    app1.py;
    app2.py;
end

subgraph p[presenter];
    subgraph presenter.py;
        Presenter;
    end
    subgraph sidebar_presenter.py;
        SidebarPresenter;
    end
    subgraph parts_presenter.py;
        PartsPresenter;
    end
    subgraph file_presenter.py;
        FilePresenter;
    end
    subgraph register_presenter.py;
        RegisterPresenter;
    end
end

subgraph v[view];
    subgraph view.py;
        View;
    end
    subgraph sidebar_view.py;
        SidebarView;
    end
    subgraph parts_view.py;
        PartsView;
        PartsXxxView;
    end
    subgraph file_view.py;
        FileView;
        FileXxxView;
    end
    subgraph register_view.py;
        RegisterView;
        RegisterConfirmView;
    end
end
```

次に、modelの構成と、modelとpresenterの依存関係を以下に示す。
- modelはpresenter以外のコンポーネントと依存関係がない。
- modelはクラス内の関数毎で依存関係が大きく異なるため、関数のレベルまで分割して記載している。
    - クラス自体は関数をまとめている箱のような役割しかしておらず、注目しなくてよい。


```mermaid
graph LR;

PartsPresenter --> add_xxx_api;
PartsPresenter --> add_yyy_api;

subgraph p[presenter];
    subgraph presenter.py;
        Presenter;
    end
    subgraph sidebar_presenter.py;
        SidebarPresenter;
    end
    subgraph parts_presenter.py;
        PartsPresenter;
    end
    subgraph file_presenter.py;
        FilePresenter;
    end
    subgraph register_presenter.py;
        RegisterPresenter;
    end
end

subgraph m[model];
    subgraph parts_crud.py;
    subgraph PartsCRUD;
        add_yyy_api;
        add_xxx_api;
        edit_parts_api;
        delete_parts_api;
        import_parts_api;
        parts_filter;
    end
    end
    subgraph file_crud.py;
    subgraph FileCRUD;
        add_file_api;
        edit_file_api;
        delete_file_api;
        import_file_api;
        file_filter;
    end
    end
end
```




## 相談
- MVP適用前後のコードを比較しながら説明する機会を設けたい
- 組み合わせを選ぶUIは表２つか？縦？横？
- アイコン+helpのUIはどうか？
- まだ試せていないこと
    - ポーリングの実装（フロント側の挙動確認）
    - ログイン/ログアウトの画面遷移
    - ヘッダー領域について
        - 配置すべき内容
        - 配置する方法
    - テストコードの作成
    - トップページの構成
    - Reactによるコンポーネント開発
        - アイコンの線の太さ
        - ウィジェット配置
        - MUI
    - キャッシュとか（よくわかっていない）

## todo
- マルチページ化
- 命名直す
    - files -> file
    - app1 -> xxxx
- チェックボックスをトグルにする
- icon修正（emoji → material icon）
    - cf: plumbing, package, deployed code
- 上の図を完成させる
    - df_configとかも整理する


## その他メモ
### CodeRabbit
- [噂のAIレビューをAzure OpenAIでできるようにしてみた](https://zenn.dev/wisteria30/articles/0930e6318aff58)
- [CodeRabbit を１ヵ月開発チームで実際に使ってみました！](https://zenn.dev/lovegraph/articles/48a3b7288299a2)

### material ui
- [Material Symbols & Icons - Google Fonts](https://fonts.google.com/icons)

### コーディング
- [可読性の高いコードを書くための実践ガイド](https://qiita.com/nucomiya/items/54d716729ffa47312f0d)
- [保守性の高いソフトウェア開発のTips集](https://zenn.dev/riku/books/36d9873ee1c0e6)

### React
- [【完全版】これ1本でReactの基本がマスターできる！初心者チュートリアル！](https://qiita.com/Sicut_study/items/d520f9a858506b81e874)


