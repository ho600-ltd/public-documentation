程式開發流程
================================================================================

.. note::

    ** 聲明 **

    本文件的閱讀對象為敝司業主、潛在業主、熱忱的未來應聘者及任何對敝司抱有興趣之活人，\
    目的乃宣揚敝司管理制度及經營理念。敝司員工當以 private-docs/software/programming.rst 為執行準則。

Git 儲存庫操作
--------------------------------------------------------------------------------

每一個 Git 儲存庫的 master branch ，預設就是對應到真實上線網站所使用的 branch 。\
通常也會有一個 dev-deploy branch 對應到測試網站。\
目前只開放系統管理員(也就是 hoamon )可以作 git push origin master(or other productional branches) \
的指令，其他開發人員都是自開 <creator_name>-feature-XXX 或 \
<creator_name>-bugfix-YYY 來作程式碼的修改。\
branch 開發完成後以 bitbucket pull request 通告系統管理員作 merge 。

所有新創功能、新觀念、新任務所使用 branch ，就歸類在 <creator_name>-feature-XXX ，\
而 <creator_name>-bugfix-YYY 皆是從 master 分枝而來，\
目的是解決真實上線網站上的「文句修正」、「臭蟲修正」等。

每一個 branch ， \
**原則上只針對一個主要目標，並不適宜將多個新創功能或臭蟲修正混在一個 branch 中** ，\
因為這些新創功能可以是分批依序 merge 進 master 的，如果只混在一個 branch 中，\
就必須待該 branch 所有新創功能全部完工後，才能作一次 merge ，\
這樣與 `最簡可行產品原則 <https://zh.wikipedia.org/wiki/%E6%9C%80%E7%B0%A1%E5%8F%AF%E8%A1%8C%E7%94%A2%E5%93%81>`_ 衝突。\
而臭蟲修正也有優先權考量，混在同一個 branch 中，\
高優先權的修正會被低優先權的影響到 merge 時程。

因 **一 branch 只針對一個主要目標** 原則，我們多半讓 branch 是基於 bitbucket issue \
來創建的。在 branch 上作文件、測試函式、程件碼的撰寫，在 issue 上作進度、責任的控管。

開發者創建 branch 後，待任務完成，首先要將該 branch 合併進 dev-deploy branch \
來測試發佈。在發佈伺服器可正確發佈該 dev-deploy branch 後，才發出 pull request ，\
由 reviewers 決定是否可 merge into master 。

因為在內部開發上，大家多運作 branch (非 fork )來工作，所以當遇到較長時間的工作中斷(\
如: 用餐、放假、出外洽公…)前，務必先將手頭的修改作一個 commit ，儘早 push 該 branch 。\
這麼作，有兩個好處:

1. 不怕程式碼被洗掉，人生總要意外，誰曉得會不會出去吃個飯，結果遭了小偷，不只丟了電腦，也丟了程式碼。
#. 儘早把程式碼 push ，其他相關人有空可以先了解一下，開發方向是否有問題。

我們主要使用 Bitbucket 作程式碼開發，但在程式碼發佈到網站的階段，\
我們的 deployment server 是拿 AWS codecommit 儲存庫來抓取新版程式碼的，\
Bitbucket 到 Codecommit 是依賴 bitbucket pipeline 作 commits 同步的工作。\
所以 **對於已 push 的 commits 不能作任何形式的 reset 操作** ，\
這會讓 pipeline 無法 push 後來的 commits 到 codecommit 。

SOP on branch and merge
--------------------------------------------------------------------------------

1. Create bitbucket issue for bug/feature/proposal/task，ex: Repository Slug=GA, Kind=enhancement(feature), Assignee=hoamon, Title=Add Pipeline Settings, No.=30
#. Create branch from master(or other major branch, depends on project setup), and the branch name should be GA#30-<assignee>-feature-add-pipeline-settings as the above condition
#. Write the document about this #30 issue in appropriate .rst
#. Discussing in issue #30 around the document, then decide the appropriate implementation method
#. Programming and discussing in docuemnt or bitbucket issue
#. Merge GA#30-<assignee>-feature-add-pipeline-settings into dev-deploy branch(ex: dev-deploy-01, test-deploy-01, test-deploy-02-for-ccgateway3, choosing branch depends on project) after finishing programming
#. Deploy with deployment server(Jenkins) and test in test web site
#. The assignee finish the source code of the feature/bugfix branch, then create a pull request ticket to "system administrator" with:
    * "deployment no.(or just paste the link from the deployment server)
    * some descriptions
    * reviewers(usually, it is system administrator)
    * decide "Closing branch or not"
    * if there is no code conflict, then the assignee **approve this new pull request**
#. If this new pull request XX **has "source code conflict"** , then the assignee should resolve it manually:
    * a case: if the source branch was branch from the target branch directly
        * step 1-a, just rebase the source branch from the target branch or merge the target branch into source branch, then resolve the conflict manually
        * step 2-a, push the new commit of the source branch
        * step 3-a, check the "conflict status", if it resolved, then **approve this pull reqeust XX** , otherwise execute step1-a ~ step2-a again
    * b case: if the source branch was **not** branch from the target branch directly
        * step 0-b, decline this new pull request XX, because bitbucket web has no "resolve conflict tool", the assignee should resolve this conflict in local computer
        * step 1-b, checkout a new branch from the HEAD of target branch(ex: master), and name this branch as prXX-<assignee>-<target_branch>. pr means "pull request", and XX means the declined pull request number.
        * step 2-b, merge the HEAD of source branch(ex: GA#30-<assignee>-feature-add-pipeline-settings) into prXX-<assignee>-master branch, then resolve the conflict manually
        * step 3-b, push the new prXX-<assignee>-master branch
        * step 4-b, create another pull request(from this prXX-<assignee>-master into master)
        * step 5-b, check the "conflict status" of the new pull request YY, if it has no conflict sources, then **approve this pull reqeust YY** and pass the issue about this pull request to reviewer
#. The reviewers(Administrators) can check the codes in pull request, the reviewers should **approve** this pull request if all reviewers confirm this pull request.  Then merge it, and deploy this new merge commit with deployment server(Jenkins or Buildbot) for testing.
#. Schedule a date to deploy this new merge to productional web site
#. If new source code serving well, then resolve the issue, otherwise run the above steps again

專案儲存庫及文件儲存庫
--------------------------------------------------------------------------------

Bitbucket/Github 都有在專案中分離 wiki 為獨立的儲存庫，我們會利用這個特性，\
把該專案相關的公開文件撰寫工作都歸納到 wiki 儲存庫，並以 sphinx 工具來編寫文件。\
私有文件則同樣置於儲存庫中的 private-docs 資料夾。

開發環境
--------------------------------------------------------------------------------

一個 Django-based 軟體專案的相關資料夾及檔案位置如下:

.. code-block:: raw

    <project-repository>/
        .<project-repository>-env/
        <project-wiki-repository>/
            requirements.txt
        <private-docs-repository>/
            index.rst
        <module-directory>/
            <app1-directory>/
            <app2-directory>/
            manage.py
            wsgi.py
        setup.py
        README.md
        private_requirements.txt
        requirements.txt

開發時，皆須使用 virtualenv 建構 .py2env  or .py3env，\
並依 <project-respository>/private_requirements.txt, <project-respository>/requirements.txt \
安裝套件。

強制使用 virtualenv 開發，有兩個好處:

1. 不同平台對 shell 的設定是有差別的，如: Windows/MacOS 在 PATH 變數上的設定，皆需由使用者自行設定，與其依賴手動調整，不如全套用 virtualenv 的環境，讓 virtualenv 自動化設定。
#. 開發環境在使用 virtualenv 後，可方便其他開發人員快速建置自己的開發環境，且系統在發佈時，也需有一「正確」的執行環境，利用 virtualenv + requirements.txt 可降低發佈失敗率
