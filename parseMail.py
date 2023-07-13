import pandas as pd
import re
body = '''<div dir="ltr">



<p style="line-height:108%;margin-bottom:0.11in;direction:ltr;background:transparent">
<br>
<br>

</p>
<table width="499" cellpadding="7" cellspacing="0">
        <colgroup><col width="110">

        <col width="111">

        <col width="111">

        <col width="110">

        </colgroup><tbody><tr valign="top">
                <td width="110" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>Source
                        software</b></font></font></p>
                </td>
                <td width="111" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>Target
                        software</b></font></font></p>
                </td>
                <td width="111" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>Binary
                        Name</b></font></font></p>
                </td>
                <td width="110" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>Binary
                        size</b></font></font></p>
                </td>
        </tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr valign="top">
                <td width="110" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>ABC</b></font></font></p>
                </td>
                <td width="111" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>GHI</b></font></font></p>
                </td>
                <td width="111" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>ABC_GHI</b></font></font></p>
                </td>
                <td width="110" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>567</b></font></font></p>
                </td>
        </tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr valign="top">
                <td width="110" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>DEF</b></font></font></p>
                </td>
                <td width="111" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>GHI</b></font></font></p>
                </td>
                <td width="111" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>DEF_GHI</b></font></font></p>
                </td>
                <td width="110" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>981</b></font></font></p>
                </td>
        </tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr></tr>
        <tr valign="top">
                <td width="110" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>ACE</b></font></font></p>
                </td>
                <td width="111" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>GHI</b></font></font></p>
                </td>
                <td width="111" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>ACE_GHI</b></font></font></p>
                </td>
                <td width="110" style="border:1px solid rgb(0,0,0);padding:0in 0.08in"><p align="center" style="line-height:115%;margin-bottom:0.1in;direction:ltr;background:transparent">
                        <font face="Calibri, serif"><font style="font-size:11pt"><b>234</b></font></font></p>
                </td>
        </tr>
</tbody></table>
<p style="line-height:108%;margin-bottom:0.11in;direction:ltr;background:transparent"><br>
<br>

</p></div>'''

def bodyParser(body):
    table_MN = pd.read_html(body.replace("<tr></tr>", ""), header =0)
    print(f'Total tables: {len(table_MN)}')
    df = table_MN[0]
    data = {
        'source': df['Source  software'].to_json(),
        'target': df['Target  software'].to_json(),
        'binary': df['Binary  Name'].to_json(),
        'size': df['Binary  size'].to_json()
    }
    return data



def subjectParse(subject):
    # Extracting data using regular expressions
    result = re.match(r"\[(.*?)\] \[(.*?)\] (\d+) \((.*?)\) (.*?) (\d+/\d+/\d+)", subject)

    if result:
        data = {
        'status' : result.group(1),
        'model' : result.group(2),
        'number' : result.group(3),
        'upgrade' : result.group(4),
        'request' : result.group(5),
        'date' : result.group(6)
        }
        return data
    else:
        print("No match found.")

from pprint import pp
pp(bodyParser(body))
pp(subjectParse("[NEW] [SM-G731U] 21 (OS_Upgrade) Submission Data Request 7/10/2023"))