Option Compare Database
Option Explicit

Private m_table_name As String
Private m_dbs As DAO.Database

Private Sub Class_Initialize()

Debug.Print "---- Class Initialized! ----"

Set m_dbs = CurrentDb()


End Sub
Property Get tblname() As String

    tblname = m_table_name

End Property
Property Let tblname(v As String)

    m_table_name = v

End Property
Function select_statement()

Dim strSelect As String
Dim intFieldCount As Integer
Dim fld As DAO.Field
Dim i As Integer

Dim strSelectStatement As String

i = 1

strSelectStatement = "SELECT " & Chr$(13)

intFieldCount = m_dbs.TableDefs(m_table_name).Fields.Count

Debug.Print "Table Name: " & m_table_name
Debug.Print "Number of fields: " & m_dbs.TableDefs(m_table_name).Fields.Count

For Each fld In m_dbs.TableDefs(m_table_name).Fields
    If i < m_dbs.TableDefs(m_table_name).Fields.Count Then
        strSelectStatement = strSelectStatement & Chr$(9) & "t." & fld.Name & ", " & Chr$(13)
        i = i + 1
    Else
        strSelectStatement = strSelectStatement & Chr$(9) & "t." & fld.Name & Chr$(13)
        i = i + 1
    End If
Next fld

strSelectStatement = strSelectStatement & "FROM " & Chr$(13) & Chr$(9) & m_table_name & " t; "

select_statement = strSelectStatement

End Function

Private Sub Class_Terminate()

m_dbs.Close

Set m_dbs = Nothing

Debug.Print "---- Class Terminated! ----"

End Sub


