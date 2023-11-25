Option Compare Database
Option Explicit

Private m_intTestVar As Integer
Private m_strDate As String
Private m_qdef_name As String
Private m_dbs As DAO.Database
Private m_strSQL As String
Private Sub Class_Initialize()

    Debug.Print "---- Class Initialized! ----"
    
    m_qdef_name = "qry_update_date_sid"
    m_strSQL = "<SQL Not Generated>"
    
    Set m_dbs = CurrentDb()
    
End Sub
Property Get strDate() As String

    strDate = m_strDate

End Property
Property Let strDate(v As String)

    m_strDate = v

End Property
Property Get qdef_name() As String

    qdef_name = m_qdef_name

End Property
Property Let qdef_name(s As String)

    m_qdef_name = s

End Property
Property Get strSQL() As String

    strSQL = m_strSQL

End Property
Sub update_query()

Dim intLower As Integer
Dim intUpper As Integer
Dim intSID_adj As Integer
Dim intLast_SID As Integer
Dim strDate As String
Dim strSQL_Where As String
Dim strSQL As String

Dim qdef As DAO.QueryDef

Set qdef = m_dbs.QueryDefs(m_qdef_name)

'Note: Function get_bound is a function in Module1
intLower = get_bound(1)
intUpper = get_bound(2)

'ID Range for update
strSQL_Where = "m.ID>=" & intLower & " AND " & "m.ID<=" & intUpper

'Change this date to reflect the working date.
strDate = m_strDate

'Adjust SID by this number.
intLast_SID = last_sid()

'Set the adjustment to 0
intSID_adj = 0
If intLast_SID > 1 Then
    intSID_adj = intLast_SID - 1
End If

'FINAL SQL Statement
If intSID_adj = 0 Then
    strSQL = "UPDATE qry_movies_edit_main_filterx_tracking AS m SET m.download_date = " & strDate & " WHERE " & strSQL_Where & ";"
    m_strSQL = strSQL
Else
    strSQL = "UPDATE qry_movies_edit_main_filterx_tracking AS m SET m.download_date = " & strDate & ", m.series_id = [series_id]-" & intSID_adj & " WHERE " & strSQL_Where & ";"
    m_strSQL = strSQL
End If

'Update Query Def with new SQL statement.
qdef.SQL = strSQL

Cleanup:

qdef.Close

Set qdef = Nothing

End Sub
Private Sub Class_Terminate()

m_dbs.Close

Set m_dbs = Nothing

Debug.Print "---- Class Terminated! ----"

End Sub
