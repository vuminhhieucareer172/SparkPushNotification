import json
import smtplib
import ssl
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from typing import List

from tabulate import tabulate

from backend.schemas.configuration import ConfigEmail


def email_sender(source: ConfigEmail, email_destination: str, subject: str, content: List[str], query=''):
    try:
        countData = len(content)
        jsonData = []
        for record in content:
            record = json.loads(record)
            record_key = record.keys()
            break
        for record in content:
            jsonData.append(json.loads(record))
        msg = MIMEMultipart("alternative")
        # msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = source.email
        msg['To'] = email_destination
        if countData > 0:
            if ('company_name' in record_key) and ('locations' in record_key) and ('position' in record_key):
                msg = MIMEMultipart("alternative")
                # msg = EmailMessage()
                msg['Subject'] = subject
                msg['From'] = source.email
                msg['To'] = email_destination
                html = """\
                                <html>
                                  <body>
                                        <div class="row">
                                    <table style="background-color:#f3f2ef;table-layout:fixed" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#F3F2EF" align="center">
                                        <tbody>
                                            <tr>
                                                <td style="padding-top:24px" align="center">
                                                    <center style="width:100%">
                                                        <table class="m_3208811051686097159mercado-email-container" style="background-color:#ffffff;margin:0 auto;max-width:512px;width:inherit" width="512" cellspacing="0" cellpadding="0" border="0">
                                                            <tbody>
                                                                <tr>
                                                                    <td style="background-color:#ffffff;padding:18px 24px 0 24px" bgcolor="#FFFFFF">
                                                                        <table role="presentation" style="width:100%!important;min-width:100%!important" width="100%" cellspacing="0" cellpadding="0" border="0">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td valign="middle" align="left">
                                                                                        <a style="color:#0a66c2;display:inline-block;text-decoration:none">
                                                                                            <img class="CToWUd" style="max-height:38px;outline:none;color:#ffffff;max-width:unset!important;text-decoration:none" height="38" border="0" src="https://cam.soict.ai/images/logo-soict.png">
                                                                                        </a>
                                                                                    </td>
                                                                                    <td width="100%" valign="middle" align="right">
                                                                                        <a style="margin:0;color:#0a66c2;display:inline-block;text-decoration:none">
                                                                                            <p style="margin:0;font-weight:400">
                                                                                                <span style="word-wrap:break-word;color:#000000;word-break:break-word;font-weight:400;font-size:14px;line-height:1.429">Nguyen Tien - Vu Hieu</span>
                                                                                            </p>
                                                                                        </a>
                                                                                    </td>
                                                                                </tr>
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td>
                                                                        <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                                                            <tbody>
                                                                                <tr>
                                                                                    <td style="padding:24px 24px 8px">
                                                                                        <h2 style="text-align:center;margin:0;color:#000000;font-weight:400;font-size:24px;line-height:1.333"><span style="color:#242424;display:inline;text-decoration:none">Your job alert</span></h2>
                                                                                    </td>
                                                                                </tr>
                                                                                """

                html += """\
                                    <tr>
                                        <td style="padding:0 24px 16px">
                                            <p style="text-align:center;margin:0;color:#000000;font-weight:400;font-size:16px;line-height:1.5">
                                                {} new job matches your preferences.
                                            </p>
                                        </td>
                                    </tr>
                                """.format(countData)

                for matching in content:
                    matching = json.loads(matching)

                    html += """\
                                        <tr>
                                            <td>
                                                <table style="padding:10px 24px" cellspacing="0" cellpadding="0">
                                                    <tbody style="table-layout:fixed;vertical-align:top;width:100%" valign="top">
                                                        <tr>
                                                            <td style="width:56px;padding-right:16px" width="56">
                                                                <a style="color:#0a66c2;display:inline-block;text-decoration:none">
                                                                    <img class="CToWUd" style="outline:none;color:#ffffff;max-width:unset!important;text-decoration:none" width="48" height="48" border="0" src="https://itrithuc.vn/vn-uploads/organization/2020_09/3tzwdpib79ogubc8ortvfktopfqg7cmn.jpeg">
                                                                </a>
                                                            </td>
                                                            <td style="padding-left:0;text-align:left" align="left">
                                                                <a style="color:#0a66c2;display:inline-block;text-decoration:none">
                                                                    <table role="presentation" valign="top" style="table-layout:fixed;vertical-align:top;width:100%" width="100%" cellspacing="0" cellpadding="0" border="0">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td style="padding-bottom:4px">
                                                                                    <a style="color:#0a66c2;font-weight:700;text-decoration:none;display:inline-block;font-size:16px">{} - {}
                                                                                    </a>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td>
                                                                                    <p style="margin:0;color:#000000;font-weight:400;font-size:14px;line-height:1.429">Position: {}</p>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td style="padding-top:8px;width:100%" width="100%"></td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                            </td>
                                        </tr>
                                    """.format(str(matching['company_name']), str(matching['locations']),
                                               str(matching['position']))

                html += """\
                                                                            </tbody>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </tbody>
                                                        </table>
                                                    </center>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                    </div>
                                  </body>
                                </html>
                                """

                part2 = MIMEText(html, "html")
                msg.attach(part2)
            else:
                # elif 'where' in query.sql or 'group by' in query.sql:
                msg = MIMEMultipart("alternative")
                # msg = EmailMessage()
                msg['Subject'] = subject
                msg['From'] = source.email
                msg['To'] = email_destination

                # html = """\
                # <table border="1">
                #     <tr>
                # """

                html = """\
                <html>
                    <body>
                        <div class="row">
                            <table style="background-color:#ffffff;table-layout:fixed" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#F3F2EF" align="center">
                                <tbody>
                                    <tr>
                                        <td style="padding-top:24px" align="center">
                                            <center style="width:100%">
                                                <table>
                                                    <tbody>
                                                        <tr>
                                                            <td valign="middle" align="left">
                                                                <a style="color:#0a66c2;display:inline-block;text-decoration:none">
                                                                    <img class="CToWUd" style="max-height:38px;outline:none;color:#ffffff;max-width:unset!important;text-decoration:none" height="38" border="0" src="https://cam.soict.ai/images/logo-soict.png">
                                                                </a>
                                                            </td>
                                                            <td width="100%" valign="middle" align="right">
                                                                <a style="margin:0;color:#0a66c2;display:inline-block;text-decoration:none">
                                                                    <p style="margin:0;font-weight:400">
                                                                        <span style="word-wrap:break-word;color:#000000;word-break:break-word;font-weight:400;font-size:14px;line-height:1.429">Nguyen Tien - Vu Hieu</span>
                                                                    </p>
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                <table>
                                                    <tr>
                                                        <td>
                                                            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                                                <tbody>
                                                                    <tr>
                                                                        <td style="padding:24px 24px 8px">
                                                                            <h2 style="text-align:center;margin:0;color:#000000;font-weight:400;font-size:24px;line-height:1.333"><span style="color:#242424;display:inline;text-decoration:none">Your job alert</span></h2>
                                                                        </td>
                                                                    </tr>
                                                                    <tr>
                                                                        <td style="padding:0 24px 16px">
                                                                            <p style="text-align:center;margin:0;color:#000000;font-weight:400;font-size:16px;line-height:1.5">
                                                                                {} new job matches your preferences.
                                                                            </p>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                                <table border="1">
                                                    <tr>
                """.format(countData)

                # table header#################################
                for column in record_key:
                    html += """
                                                        <th style="text-align:center;">{}</th>
                    """.format(str(column))
                html += """
                                                    </tr>
                """
                # table header#################################

                # table content#################################
                for data in jsonData:
                    html += """
                                                    <tr>
                    """
                    for key in record_key:
                        html += """
                                                        <td style="text-align:center;">{}</td>
                        """.format(data[key])
                    html += """
                                                    </tr>
                    """
                # table content#################################

                html += """\
                                                </table>
                                            </center>
                """
                html += """\
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </body>
                </html>
                """
                # html = """{table}"""
                # html = html.format(table=tabulate(lastData, headers="keys", tablefmt="pretty"))
                part2 = MIMEText(html, "html")
                msg.attach(part2)
        else:
            msg = MIMEMultipart("alternative")
            # msg = EmailMessage()
            msg['Subject'] = subject
            msg['From'] = source.email
            msg['To'] = email_destination
            html = """\
                                            <html>
                                              <body>
                                                    <div class="row">
                                                <table style="background-color:#f3f2ef;table-layout:fixed" width="100%" cellspacing="0" cellpadding="0" border="0" bgcolor="#F3F2EF" align="center">
                                                    <tbody>
                                                        <tr>
                                                            <td style="padding-top:24px" align="center">
                                                                <center style="width:100%">
                                                                    <table class="m_3208811051686097159mercado-email-container" style="background-color:#ffffff;margin:0 auto;max-width:512px;width:inherit" width="512" cellspacing="0" cellpadding="0" border="0">
                                                                        <tbody>
                                                                            <tr>
                                                                                <td style="background-color:#ffffff;padding:18px 24px 0 24px" bgcolor="#FFFFFF">
                                                                                    <table role="presentation" style="width:100%!important;min-width:100%!important" width="100%" cellspacing="0" cellpadding="0" border="0">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td valign="middle" align="left">
                                                                                                    <a style="color:#0a66c2;display:inline-block;text-decoration:none">
                                                                                                        <img class="CToWUd" style="max-height:38px;outline:none;color:#ffffff;max-width:unset!important;text-decoration:none" height="38" border="0" src="https://cam.soict.ai/images/logo-soict.png">
                                                                                                    </a>
                                                                                                </td>
                                                                                                <td width="100%" valign="middle" align="right">
                                                                                                    <a style="margin:0;color:#0a66c2;display:inline-block;text-decoration:none">
                                                                                                        <p style="margin:0;font-weight:400">
                                                                                                            <span style="word-wrap:break-word;color:#000000;word-break:break-word;font-weight:400;font-size:14px;line-height:1.429">Nguyen Tien - Vu Hieu</span>
                                                                                                        </p>
                                                                                                    </a>
                                                                                                </td>
                                                                                            </tr>
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td>
                                                                                    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0">
                                                                                        <tbody>
                                                                                            <tr>
                                                                                                <td style="padding:24px 24px 8px">
                                                                                                    <h2 style="text-align:center;margin:0;color:#000000;font-weight:400;font-size:24px;line-height:1.333"><span style="color:#242424;display:inline;text-decoration:none">Your job alert</span></h2>
                                                                                                </td>
                                                                                            </tr>
                                                                                            """

            html += """\
                                                <tr>
                                                    <td style="padding:0 24px 16px">
                                                        <p style="text-align:center;margin:0;color:#000000;font-weight:400;font-size:16px;line-height:1.5">
                                                            {} new job matches your preferences.
                                                        </p>
                                                    </td>
                                                </tr>
                                            """.format(countData)

            for matching in content:
                matching = json.loads(matching)

                html += """\
                                                    <tr>
                                                        <td>
                                                            <table style="padding:10px 24px" cellspacing="0" cellpadding="0">
                                                                <tbody style="table-layout:fixed;vertical-align:top;width:100%" valign="top">
                                                                    <tr>
                                                                        <td style="width:56px;padding-right:16px" width="56">
                                                                            <a style="color:#0a66c2;display:inline-block;text-decoration:none">
                                                                                <img class="CToWUd" style="outline:none;color:#ffffff;max-width:unset!important;text-decoration:none" width="48" height="48" border="0" src="https://itrithuc.vn/vn-uploads/organization/2020_09/3tzwdpib79ogubc8ortvfktopfqg7cmn.jpeg">
                                                                            </a>
                                                                        </td>
                                                                        <td style="padding-left:0;text-align:left" align="left">
                                                                            <a style="color:#0a66c2;display:inline-block;text-decoration:none">
                                                                                <table role="presentation" valign="top" style="table-layout:fixed;vertical-align:top;width:100%" width="100%" cellspacing="0" cellpadding="0" border="0">
                                                                                    <tbody>
                                                                                        <tr>
                                                                                            <td style="padding-bottom:4px">
                                                                                                <a style="color:#0a66c2;font-weight:700;text-decoration:none;display:inline-block;font-size:16px">{} - {}
                                                                                                </a>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td>
                                                                                                <p style="margin:0;color:#000000;font-weight:400;font-size:14px;line-height:1.429">Position: {}</p>
                                                                                            </td>
                                                                                        </tr>
                                                                                        <tr>
                                                                                            <td style="padding-top:8px;width:100%" width="100%"></td>
                                                                                        </tr>
                                                                                    </tbody>
                                                                                </table>
                                                                            </a>
                                                                        </td>
                                                                    </tr>
                                                                </tbody>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                """.format(str(matching['company_name']), str(matching['locations']),
                                                           str(matching['position']))

            html += """\
                                                                                        </tbody>
                                                                                    </table>
                                                                                </td>
                                                                            </tr>
                                                                        </tbody>
                                                                    </table>
                                                                </center>
                                                            </td>
                                                        </tr>
                                                    </tbody>
                                                </table>
                                                </div>
                                              </body>
                                            </html>
                                            """

            part2 = MIMEText(html, "html")
            msg.attach(part2)

        # part2 = MIMEText(html, "html")
        # msg.attach(part2)

        # msg.set_content(content)
        context = ssl.create_default_context()
        if source.ssl:
            server = smtplib.SMTP_SSL(host=source.host, port=source.port, context=context)
        else:
            server = smtplib.SMTP(host=source.host, port=source.port)
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
        server.login(source.username, source.password)
        # server.sendmail(
        #     source.email, email_destination, msg.as_string()
        # )
        server.send_message(msg)
        server.quit()
        return "Completed"
    except Exception as e:
        print(e)
        raise e

# if __name__ == '__main__':
#     email_sender(source=ConfigEmail(
#             host="smtp.gmail.com",
#             port=465,
#             email="vuminhhieucareer172@gmail.com",
#             username="vuminhhieucareer172@gmail.com",
#             password="0352428080",
#             ssl=True),
#         email_destination="vuminhhieucareer172@gmail.com",
#         subject="Your job alert",
#         content=["'application_deadline':'30/12/2022', 'company_address':'101 Láng Hạ', 'company_name':'Vinetek', 'salary': '21', 'position': 'AI Engineer', 'year_experience': '1 năm'",
#                  "'application_deadline':'30/12/2022', 'company_address':'101 Láng Hạ', 'company_name':'Vinetek', 'salary': '22', 'position': 'Data Engineer', 'year_experience': '1 năm'"],
#     )
