import gspread


def rec_to_sheets(data):
    fsa = "service_account.json"
    sa = gspread.service_account(fsa)
    sh = sa.open("Design_lab_orders")

    wsh = sh.worksheet('Data')
    wsh.append_row(list(data.values()))
    return True


def add_user_info(data):
    fsa = "service_account.json"
    sa = gspread.service_account(fsa)
    sh = sa.open("Design_lab_orders")

    wsh = sh.worksheet('Users')
    wsh.append_row(list(data.values()))
    return


def check_user(u_id: str):
    fsa = "service_account.json"
    sa = gspread.service_account(fsa)
    sh = sa.open("Design_lab_orders")
    wsh = sh.worksheet('Users')
    #     get A col values
    cnt_A = wsh.col_values(1)
    name_from_sheet = ""
    for i in cnt_A:
        if i == u_id:
            name_from_sheet = wsh.row_values(cnt_A.index(i)+1)[1]
    print(f'name_from_sheet is {name_from_sheet}')
    return name_from_sheet
