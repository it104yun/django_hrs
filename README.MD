# **hrs** **: `H`uman `R`esource `S`ystem**

- (1)-因應日後KPI、BSC系統化的需求,預先將本專案取名為hrs,以避免1個app佔用一個project的狀況發生。
- (2)-日後或許會有其他需求 : 例如教育訓練或考積管理,分紅管理.... 。 

**`recruiter`** : 新人報到app 未來希望做到 : 面試->錄取->報到…等一貫作業,讓app符合**『招募』**精神, 所以新人報到app『先』取名recruiter 。

 

## ***進度***log***<br/>
## `２０２０年`
| **PUSH NO** | **PUSH DATE**  | **CONTENT**                                                  |
| ------ | --------- | ------------------------------------------------------------------------------------------- |
| 1      | 7/7~7/22  | ORM調整、測試完成                                            |
| 2      | 7/23~7/24 | 多語系架構建立                                               |
| 3      | 7/27      | Admin site 整理設定完成                                      |
| 4      | 7/27      | 上git之後, 先轉往『KPI模組』工作                             |
| 5      | 7/31      | 1-新增app : kpi<br />2-model : 已建立完成<br />           EmployeeEasyInfo,<br />           MetricsSetup,<br />           MetricsCalc,<br />           ScoreSheet,<br />           EeAttendDetails,<br />           EeAttendSummary<br />3-admin.site : 編輯完成, 測試完成<br />4-app : common的修改<br />model : 增加TopicOfUdc,簡化UserDefCode<br /><br />修改相對應的limit_choices_to={'topic_code':'......'}<br /> |
| 6      | 8/28      | 系統作業 : SY011,SY110功能全部完成<br/>     /人事/出勤作業FORM/TEMPLATE已完成                                                            |
| 7      | 9/4       | 全部完成:系統作業--sy011,sy110,sy120,sy130<br/>    form&(新增/刪除/修改/查詢)可運作:hr01,hr03,hr05,bs01     <br/>form&(查詢)可運作:bs03
| 8      | 9/22      | form&(新增/刪除/修改/查詢)可運作: 增加bs03,sc01<br>------其中:sc01流程已順利      |
| 9      | 9/23~10/30     |9/28~9/30 forms 美化,排版<br />10/6~10/12 程式優化<br />10/13~10/14  Django 與 PostgresSQL 10.14<br />　　　(1).安裝PostgresSQL<br />　　　(2).改寫Django setting.py程式<br />　　　(3).資料庫移轉<br />　　　(4).資料匯入<br />10/14~10/16 程式撰寫 : excel匯入( 人事基本資料)<br />10/19~10/20 程式撰寫 : excel匯入( 人事基本資料),已完成<br />10/21~10/23 程式撰寫 : 資料複製( 人事基本資料)<br />10/26~10/27 程式撰寫 : 改為-->批量<bulk_create>複製( 人事基本資料),已完成<br />10/26~10/27 10/28~10/29 程式撰寫 : excel匯入( 出勤資料匯總),已完成|
|10      |10/29~11/27     |指標設定/指標計算方式設定已完成|      
|11      |11/30~12/21     |自評(實績)/主管審核/現行年月設定...已完成|    
|12      |12/22     | hrs\requirements 加入 requirements.txt|     
 
 
## `2021年`
| **PUSH NO** | **PUSH DATE**  | **CONTENT**                                                  |
| ------ | --------- | ------------------------------------------------------------------------------------------- |
|14      |1/1~3/22|01-調整程式代號　(1)統一為5碼　(2)編號改為PM開頭<br />02-權限管控 : 只有「直屬主管」可以處理下屬的KPI<br />03-「績效列印」完成75% <br />04-新增功能項(未開始):<br />　　(1)人事(共同衡量指標)<br />　　(2)教育訓練彙總<br />　　(3)年月關帳<br />　　(4)共同衡量指標設定<br />　　(5)共同計算方式設定<br />　　(6)人資檢核    <br />05-大量防呆控制<br />06-速度的改善<br />|
|15      |3/23|加入gitignore，清除192.168.100.220\hrs的所有資料，重新上一次專案。|   
|16      |3/24|修改pm208.js，pm210.js :當年度無任何指標時的處理方式（ rows=0 ）。|  
|17      |4/21|新增程式pm204:共同衡量指標設定,pm206:共同計算方式設定| 
|18      |4/23|更正gitignore的路徑及內容| 
|19      |4/23|刪除本地端的專案,重新<br>git clone http://192.168.5.224/itg2/hrs.git <br>***因應加入gitignore*** <br>本機端做了以下動作 <br>git rm -r --cached .<br>git add .<br>git commit -m README.MD<br>git push origin HEAD:master|      
|20      |4/27|PM402-KPI自評/PM406-KPI主管審核:依共同指標的『評核類型』決定是否顯示-->修改完成。<br><br>bug的修正:<ol><li>Employee無資料(但有帳號)的錯誤畫面<li>ldap無帳號的錯誤畫面</ol>|   
|21      |5/4|P208,PM210無法新增的錯誤修正<br>關帳檢核已完成(已產生excel檔,但還無法下載)| 
|22      |5/5|PM203-評核年月關帳：已可產生檢核檔，且會自動開啟檢核檔| 
|23      |5/6|PM004-人事基本資料:資加欄位－『領獎金方式、直接／間接』－『bonus_type、labor_type| 
|24      |5/12~5/13|PM004人事基本資料:<ol><li>離職日預設改為None<li>濾掉評核主管"共同指標"的工號<li>自動判斷職等,自動選取BSC/KPI<li>匯人:原本只可新增,為配合日後人事資料異動,改成亦可修改</ol>| 
|25      |5/14|PM203 評核年月關帳:增加欄位,判斷那些狀態該匯出至EXCEL  |
|26      |5/17|PM203 評核年月關帳:狀態"BPM簽核完成"前都要列出。<br><b>**<u>PM203評核年月關帳,至此已全部完成</u>**</b>|  
|27      |5/18|<ol><li>PM204 KPI共同衡量指標:『"新增"按鈕』不論任何年月都打開，加入『小於評核年月』的防呆。<br><li>PM206 KPI共同計算方式:新增3個"顯示資料"按鈕,因於程式開啟並同時載入資料,速度太過緩慢,因此由使用者控制何時載入資料。</ol>|
|28      |5/19~5/21|<ol><li>速度緩慢原因追查:ForeignKey在web載入時，將全部的relation data載入，可以在forms.py把＂欄位＂初值指定為空，可避免。<ul><li>PM204/PM208(KPI衡量指標設定)<br>self.fields['work_code'] = forms.ChoiceField(choices=[])<li>PM206/PM210(KPI計算方式設定)<br>self.fields['metrics'] = forms.ChoiceField(choices=[]) </ul><li>PM208 KPI衡量指標設定:<ul><li>『"新增"按鈕』不論任何年月都打開，加入『小於評核年月』的防呆。<li>新增3個"顯示資料"按鈕,因於程式開啟並同時載入資料,速度太過緩慢,因此由使用者控制何時載入資料。<li>共同指標不計入配分100限制(order_number>900)</ul><li>PM210 KPI計算方式設定:<ul><li>新增3個"顯示資料"按鈕,因於程式開啟並同時載入資料,速度太過緩慢,因此由使用者控制何時載入資料。<li>而後又取消,因已找到問題徵結點,因應項目1的修改,在.js中加入控制碼)</ul><li>PM004 人事基本資料:增加e-mail欄位ul5-上傳server前,測試<ul><li>PM0004 人事基本資料：OK</ul></ol>|
|29      |5/24~5/31|繼續測試<ul><li>衡量指標(共同/個人):複製,展開,收回Dialog防呆<li>衡量指標(共同):展開至員工/收回,加入部門及工號的選擇</ul>|
|30      |5/31~6/2|<ol><li>衡量指標(共同.個人)展閞、複製<ul><li>沒處理的欄位(新增的)。<li>挑選的工號沒檢查到所有指標「是否都有」計算方式<li>「展開」只做大於評核的當年月<li>衡量指標、部門、工號...只能用挑選,禁止輸入</ul><li>自評,主管審核<ul><li>月份:無法顯示的問題<li>每一個subDetail增加「確定」按鈕<li>避免在存檔前, 最後一次的修改, 沒有寫進資料庫<li>儲存更新、送出:一整筆只Alert『一整筆』的處理結果<li>送出:email通知,改抓人事基本資料檔的email</ul></ol>|
|31      |6/3~6/25|<ol><li>增加程式 : PM802 衡量指標查詢/PM806 評核查詢(人資)<li>計算方式防呆程式設計<li>page在各種不同螢幕上的測試和調整<li>更改base.html<li>PM204/PM206:加入最低配分的處理</ol>|      
|32      |6/25|<ul><li>新增程式<ol><li>cm002:自定義碼主題<li>cm004:自定義碼設定</ol><li><ol><li>增加"common"進ldap_auth\extension.py的路徑<li>修改reports的位置:新的..media-files/reports<li>承上:修改pm203/pm602/pm604/pm606報表的存檔位置至media-files</ol>(2,3)乃為試著解決在python server無權限開啟.xlsx及.pdf的問題</ul>|
|33      |6/28~7/2|<ul><li>PM208:KPI衡量指標設定<ol><li>加入「批次刪除」功能按鈕<li>加入「得分(遞增/遞減)」</ol><li>增加程式:<ol><li>CM002:自定義碼主題<li>CM004:自定義碼設定</ol><li>add fields<ol><li>system-factory:「description」公司全名<li>common-UserDefCode:「description」因應部門全稱太長了<li>kpi-EmployeeInfoEasy:「dept_flevel / dept_desc / direct_supv / factory_area / service_status / service_status」 一級部門 / 部門全稱 / 直接主管 / 廠區 / 服務狀態(正式員工,試用員工)</ol><li>python server已可開啟excel,pdf</ul>|
|34      |7/5|<ul><li>system add fields-->model:Factory<ol><li>nat:公司所在國<li>address:公司住址</ol></ul>| 
|35      |7/6~7/9|**PM004人事基本資料,增加查詢**<ul><li>功能開啟時不載入資料<ol><li>autoload:false<li>在『搜尋』按紐按下後,autoload:true</ol><li>查詢欄位(可泛查,單選):員工,主管,部門<li>按鈕:搜尋,清除選擇<li>加入公司區隔<ol><li>用那個公司登入，只能看該範圍的人事資料<li>複製員工，搜尋選擇(員工/主管)</ol></ul>**單筆刪除防呆(按下刪除後,詢問是否確定刪除)**<ul><li>PM004 人事基本資料<li>PM204 KPI共同衡量指標<li>PM206 KPI共同計算方式設定<li>PM208 KPI衡量指標設定<li>PM210 KPI計算方式設定</ul>| 
|36      |7/12~7/14|<ul><li>PM402 KPI自評(實績):若右欄(年月欄)無資料,disable所有按鈕及input item<li>工號篩選排除,評「BSC」的員工<ol><li>PM204 共同衡量指標設定<li>PM208 衡量指標設定</ol><li>PM208 衡量指標設定:批次刪除,進入「建立新資料」後,隱藏「批次刪除」按紐</ul>|
|37      |8/2~8/6|<ul><li>系統面修改<ol><li>只要有reload(或 重新整理)就會看到他人的權限( 但無法使用 ):common\api.py system_tree:拿掉緩存<li>登入時,偵測鍵盤的大小寫</ol><li>PM004:人事不再分公司別查詢(拿掉curr_factory的param)<li>PM204 共同衡量指標設定<ol><li>收回失敗,Metricscalc的metrics之前修改為on_delete='PROTECT',加寫本檔的刪除<li>加入"共同指標"使用說明</ol><li>pm208 KPI衡量指標設定<ol><li>展開、複製不檢查共同指標<li>欄位"asc_desc_score"展開、複製沒處理到</ol><li>pm210 KPI計算方式設定：下限、上限改至小數1位<ol><li>django model 修改<li>js parseFloat...改欄位麻煩問題很多</ol><li>pm402/pm406 自評/主管審核:實績改至小數一位<ol><li>django model <li>js parseFloat...改欄位麻煩問題很多</ol><li>PM402/PM406 自評/主管審核<ol><li>只顯示評核年月的資料<li>下屬評分後"儲存更新"即備份至(bu_calc_content,bu_metrics_calc,bu_actual_score)<li>未『儲存更新』"送出紐Disable"<li>grid拿掉"確定"按紐<li>點實績偶無法編輯(js 拿掉 currentIndex!=lastIndex)<li>0顯示空白(後端給null造成)<li>評分為0"送出"顯示提醒<li>評核方式移除,改放"指標類型"</ol><li>sy120/sy130:增加查詢(泛查)<li>多螢幕畫面調整</ul>|
|38      |8/9~8/10|<ul><li>PM402-KPI自評<ol><li>"送出"，按下取消多次後，再按確定，會重覆MAIL，N+1次，已解決。<li>加入防呆:實績空白，超過範圍，alert<li>得分為0，送出前顯示警語。</ol><li>PM406-KPI主管審核<ol><li>"送出"，按下取消多次後，再按確定，會重覆MAIL，N+1次，已解決。<li>加入防呆:實績空白，超過範圍，alert<li>得分為0，送出前顯示警語。</ul>|                                                                
|39      |8/10~8/11|<ul>PM406-KPI主管審核<ol><li>"儲存更新"後跳到第一筆，改為跳到"current row"。<li>"送出"後跳到第一筆，改為跳到"current row" or "(current row)-1" <li>所有人都送出後，加入"page reload"(=F5)<li>移除"取消"按鈕</ol></ul>|
|40      |8/12~2/24|<ul>技能矩陣表<li>TT202 職務名稱維護<li>TT204 職能名稱維護<li>TT208 職務綁定職能<li>TT402 教育訓練方式維護<li>TT4061 技能盤點底稿產生<li>TT4062 技能盤點主檔<li>TT4063 技能盤點明細</ul>|
|40      |9/27~10/1|<ul>***無法自評流程,程式修改***<li>PM004 人事基本資料:加入"kpi_diy"/"skill_diy"欄位<li>PM203 評核年月關帳<ol><li>加入欄位"before_lastdate"/"diy_date"<li>檢核:本期/下期,未有衡量指標<li>本期/下期,衡量指標未滿100分/計算方式得分沒有0及最高配分/得分大於最高配分<li>產生『不可自評的工作底稿』，狀態為110(主管直接評核)</ol></ul>|
|41      |10/04~10/05|<ul><li>PM203 評核年月關帳 檢核:衡量指標無計算方式<li>base.html : 加入今天日期的版次</ul>|
|42      |10/06~10/27|<ul><li>季報表自動產生並送至BPM<ol><li>季報表暫存檔:model.py新增"ReportQuarter"<li>季報表狀態檔:model.py新增"ScoreStatus"<li>BPM串接<li>寫入上列三項資料:api_kpi_report.py "KPI_ReportQuarterView/set_bpm_number/kpi_report_quarter_temp"<li>JasperReport重拉季報表格式:KPI_PM610_ReportQuarter_Landscape.jrxml</ol><li>所有數字改到小數點以下2位,除了"order_number/order_item"<ol><li>修改MODEL FIELD的欄位型態為Decimal，小數位數至第２位<li>修改相關程式：PM204,PM206,PM208,PM210,PM402,PM406,PM802,PM806,PM610,PM620,KPI_PM610_ReportQuarter_Landscape.jrxml</ul>|
|43      |10/27~10/27|<ul><li>移除檔案EeAttendDetails<li>移除檔案EeAttendSummary</ul>|
|44      |10/28~10/28|<ul><li>api_kpi_report.py : 判斷Quarter的月份重寫。<li>pm203.js : 更新不成功remark。</ul>|
|45      |10/29~12/14|技能矩陣表,完成。|


## `2022年`
| **PUSH NO** | **PUSH DATE**  | **CONTENT**                                                  |
| ------ | --------- | ------------------------------------------------------------------------------------------- |
|46      |2021/12/15~1/14|工作事項明細表完成|   
|47      |1/17~1/18|TT602 工作事項明細表填寫，加上『匯入』功能|
|48      |1/19~1/26|技能盤點表修改| 
|49      |1/27|技能盤點表修改|
|50      |1/27~2/21|修改KPI程式PM204,PM206,PM208,PM210,PM402,PM406|    
|51      |3/4~3/15|<ul><li>工作事項明細表:匯入完成<li>技能盤點表:tt408技能盤點底稿維護(新增,刪除)<li>tt002人事基本資料,程式優化</ul>| 
|52      |3/16~3/25|<ul><li>技能盤點表tt407,tt407_2pdf,tt407.js<ol><li>有些明細未顯示,修改加入setTimeout,因為app未抓到資料,matrixstatus的狀態已變更<li>檢查填寫內容:原先只有顯示那一列有問題,改成那一格那個選項都顯示<li>離開頁面加入警告<ol></ul>| 
|53      |3/28|<ul>工作事項明細表<ol><li>tt407.js : 週期次數的cycl, editable : false<li>tt407.js : 離開頁面的警告</ol></ul>| 
|54      |3/29~3/31|<ul>績效管理管理系統<ol><li>PM806季報表送簽狀況查詢:已完成<li>季報表已產生未開啟:已解決(人資2021/1-6月已評核完成,又要重做,我只有把狀態碼恢復成未評核,但未把"SheetStatus"對應的資料刪除)</ul>| 
|55      |4/1,4/6~4/7|職務名稱大於8個時，第一個TAB的格子寬度會縮小:已解決|     
|56      |4/8|tt407.js更正在getselected選不到的錯誤|     
|57      |4/12~4/14|4/11休假<br><h5><u>績效管理系統</u></h5><ul><li>PM402-KPI自評(實績<ol><li>衡量指標加入"評核方式"<li>所有共同指標都顯示<li>共同指標="匯入實績",皆鎖住,不予修改<li>匯入實績="會議管理系統",從"會議管理系統"抓取會議評鑑的總分(加減分)</ol><li>PM406-KPI主管審核<ol><li>衡量指標加入"評核方式"<li>所有共同指標都顯示<li>共同指標="匯入實績",皆鎖住,不予修改<li>匯入實績="會議管理系統",從"會議管理系統"抓取會議評鑑的總分(加減分)</ol></ul><br><h5><u>工作事項明細表</u></h5><ul><li>TT602-工作事項明細填寫<ol><li>首次編輯無法點開 : 調整onDblClickRow "endEdit" / "beginEdit"</ol></ul>|     
|58      |4/15~4/26|<ul><li>技能盤點表:管理職能,非管理職,也能輸入,已修正。<li>工作事項明細表<ol><li>"確認/管控"儲存至"諮詢",已修正。<li>匯入後直接"送至BPM",沒有檢查異常,已修正。<li>加入填寫注意事項。<li>加入每列的錯誤檢查,即時提醒。<li>加入"匯入"注意事項。</ol><li>調整登入畫面：縮小字體。</ul>|     
|59      |4/27~5/10|<ul><li>HR-->PMS人事基本資料同步<ol><li>TT002 人事基本資料:增加按鈕"比對HR",修改程式tt002.js,api_skill.py<li>app kpi修改model.py:EmployeeInfoEasy+dept_description,+class WorkcodeMapping:TT004 HR海外工號對照表，+class DeptSupervisor:TT006 部門主管對照表</ol><li>TT602 工作事項明細填寫:移除GRID下的"填寫注意事項","週期次數(匯入才會)"挑選錯誤的檢查。</ul>|     
|60      |5/11~5/30|<ul><li>tt002 人事基本資料:增加兩個按紐<ol><li>比對hr<li>匯入</ol><li>tt002 人事基本資料:新增/刪除/查詢優化,增加按紐:開啟搜尋(queryParams模組化)</ol></ul>|            
|61      |6/1~6/22|<ul><li>TT603 工作事項明細表(代填)<br>app-->skill_pdca:api_urls_skill.py,view.py,static/static/js,statkc/statkc/template <br>(1)-TT603 (2)-TT603_TAB (3)-TT603_TAB2PDF<li>"送至BPM":將PDF下載一份至本機的個人資料夾\Downloads</ul>|     
|62      |6/25~7/5|Embed the "Google Translate Objects- google.translate.TranslateElement" function in frontend.That's embedded under the list's item programs.<ul><li>html,js<ol><li>tt062<li>tt602_2pdf_open<li>tt603<li>tt603_tab2pdf_open<li>tt626</ol></ul>|     
|63      |7/8~8/10|多國語言翻譯<ul>工作事項明細表<li>tt602,tt602_2pdf,tt603,tt603_tab,tt603_tab2pdf<li>後台admin能進入,必需在system/user建立帳戶, 進入時網址加入"/admin"可進入<ol><li>system 的user增加field<li>輸入翻譯對照,網址加入"/rosetta",每個人都可進入</ol></ul>|  
|64      |~|<ul><li></ul>|     
|65      |~|<ul><li></ul>|     
|66      |~|<ul><li></ul>|  