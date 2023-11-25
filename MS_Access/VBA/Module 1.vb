Option Compare Database
Sub add_blank_movie_records()

Dim dbs As DAO.Database
Dim qdef As DAO.QueryDef
Dim rs As DAO.Recordset
Dim i As Integer

Set dbs = CurrentDb()

Set qdef = dbs.QueryDefs("append_movie_blanks")

Set rs = dbs.OpenRecordset("select * from movies")

rs.MoveLast
rs.MoveFirst

Debug.Print "Number of records: " & rs.RecordCount

i = 5

Do While i <= 10
    qdef.Parameters("p_download_date") = #2/8/2022#
    qdef.Parameters("p_series_id") = i
    qdef.Execute
    i = i + 1
Loop

rs.Close
qdef.Close
dbs.Close

Set rs = Nothing
Set qdef = Nothing
Set dbs = Nothing

End Sub
Sub test_stored_procedure()

Dim dbs As DAO.Database
Dim qdef As DAO.QueryDef
Dim rs As DAO.Recordset

Set dbs = CurrentDb()
Set qdef = dbs.QueryDefs("pass_through_test")

Set rs = qdef.OpenRecordset()

Debug.Print "SQL Statement: " & qdef.SQL

If Not rs.EOF Then
    rs.MoveLast
    rs.MoveFirst
    Debug.Print "Number of files found: " & rs.RecordCount
Else
    MsgBox ("No record found.")
End If

End Sub
Sub test_linc()

Dim dbs As DAO.Database
Dim qdef As DAO.QueryDef
Dim str_sql As String

str_fragment = "Bro"

str_sql = "CALL find_movie_by_filename ('%" & str_fragment & "%');"

Set dbs = CurrentDb()

Set qdef = dbs.QueryDefs("pass_through_test")

Debug.Print "SQL: " & str_sql

dbs.Close
qdef.Close

Set dbs = Nothing
Set qdef = Nothing

End Sub
Sub add_blank_movie_entry(str_date As String, sid_start As Integer, sid_end As Integer)

Dim dbs As DAO.Database
Dim qdef As DAO.QueryDef
Dim rs As DAO.Recordset
Dim i As Integer

Set dbs = CurrentDb()

Set qdef = dbs.QueryDefs("pass_through_add_blanks")

i = sid_start

Do While i <= sid_end
    qdef.SQL = "CALL add_movie_blanks ('" & str_date & "', " & i & ");"
    qdef.Execute
    Debug.Print "Executed SQL: " & qdef.SQL
    ' MsgBox "New blank entries added to database.", vbOKOnly
    i = i + 1
Loop

Cleanup:

qdef.Close
dbs.Close

Set qdef = Nothing
Set dbs = Nothing

End Sub
Sub add_blank_movie_entry_run()

Call add_blank_movie_entry("2022-08-13", 3, 10)

End Sub
Sub copy_to_password()

Forms!movies1.txtbx_password.SetFocus

SendKeys "^v", True

End Sub
Sub copy_to_filename()

Forms!movies1.filename.SetFocus

SendKeys "^v", True

End Sub
Sub control_c()

SendKeys "^c", True

End Sub
Sub test_table_relinking()

Dim tbldef As DAO.TableDef
Dim dbs As DAO.Database
Dim rs As DAO.Recordset

Dim strConnect As String
Dim strTableName As String

strConnect = "ODBC; DATABASE=nzb_search_dev; UID=linc_dev; PWD=D0gP1L3$1lv8rB1g; DSN= mdb;"

Set dbs = CurrentDb()

Set rs = dbs.OpenRecordset("SELECT * FROM tbl_tables_to_relink WHERE table_connection_type_id = 1 ORDER BY ID;")

i = 1

If Not rs.EOF Then
    rs.MoveLast
    rs.MoveFirst
    Do While i <= rs.RecordCount
        strTableName = rs.Fields(1).Value
        dbs.TableDefs(strTableName).Connect = strConnect
        Debug.Print i & ") Relinked: " & strTableName
        i = i + 1
        rs.MoveNext
    Loop
End If

rs.Close
dbs.Close

Set rs = Nothing
Set dbs = Nothing

End Sub
Sub test_list_tables()

Dim tbldef As DAO.TableDef
Dim dbs As DAO.Database
Dim i As Integer

Set dbs = CurrentDb()

i = 1

For Each tbldef In dbs.TableDefs
    If tbldef.Connect = "" Then
        Debug.Print i & ") Local table: " & tbldef.Name
        i = i + 1
    Else
        Debug.Print i & ") Linked Table: " & tbldef.Name & ", " & tbldef.Connect
        i = i + 1
    End If
Next

dbs.Close
Set dbs = Nothing

End Sub
Function get_bound(intType As Integer) As Integer

'Returns the Lower and Upper ID of un-used placeholder entries in Movies table.
'Arguments:
'   - intType = 1 : Lower bound
'   - intType = 2 : Upper bound

Dim dbs As DAO.Database
Dim rs As DAO.Recordset

Dim strSQL_Upper_Bound As String
Dim strSQL_Lower_Bound As String

Set dbs = CurrentDb()

If intType = 1 Then
    strSQL_Lower_Bound = "SELECT TOP 1 m.ID FROM qry_movies_edit_main_filterx_tracking m WHERE m.blank_flag = 1 ORDER BY m.ID;"
    Set rs = dbs.OpenRecordset(strSQL_Lower_Bound)
Else
    If intType = 2 Then
        strSQL_Upper_Bound = "SELECT TOP 1 m.ID FROM qry_movies_edit_main_filterx_tracking m WHERE m.blank_flag = 1 ORDER BY m.ID DESC;"
        Set rs = dbs.OpenRecordset(strSQL_Upper_Bound)
    Else
        MsgBox "Must select 1=Lower or 2=Upper.", vbOKOnly
    End If
End If

If Not rs.EOF Then
    rs.MoveFirst
    get_bound = rs.Fields(0).Value
End If

Cleanup:

rs.Close
dbs.Close

Set rs = Nothing
Set dbs = Nothing
    
End Function
Function last_sid() As Integer

Dim dbs As DAO.Database
Dim qdef As DAO.QueryDef
Dim rs As DAO.Recordset

Set dbs = CurrentDb()
Set qdef = dbs.QueryDefs("qry_sid_start")
Set rs = qdef.OpenRecordset()

If Not rs.EOF Then
    last_sid = rs.Fields(0).Value
Else
    last_sid = 0
End If

Cleanup:

rs.Close
qdef.Close
dbs.Close

Set rs = Nothing
Set qdef = Nothing
Set dbs = Nothing

End Function
