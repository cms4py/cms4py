from .URL import URL
import tornado.httputil


def default_row_render(row, fields):
    html_str = "<tr>"
    for f in fields:
        html_str += f"<td>{row[f]}</td>"
    html_str += "</tr>"
    return html_str


def default_header_render(fields):
    html_str = "<tr>"
    for f in fields:
        html_str += f"<th>{f}</th>"
    html_str += "</tr>"
    return html_str


def default_foot_render(request: tornado.httputil.HTTPServerRequest, current_page_index, paginate, all_count):
    def create_link(page_index, label=None):
        return f"<a class='btn-page-number' href='{URL(request.path, vars=dict(page_index=page_index))}'>{(page_index + 1) if not label else label}</a>"

    last_page_index = int(all_count / paginate)
    html_str = ""
    if last_page_index > 0:
        page_number_btns = [create_link(current_page_index)]
        i = 0
        for i in range(current_page_index - 1, current_page_index - 5, -1):
            if i < 0:
                break
            page_number_btns.insert(0, create_link(i))
        if i > 0:
            page_number_btns.insert(0, create_link(0, "<<"))
        for i in range(current_page_index + 1, current_page_index + 5):
            if i > last_page_index:
                break
            page_number_btns.append(create_link(i))
        if i < last_page_index:
            page_number_btns.append(create_link(last_page_index, ">>"))
        # dump html content
        html_str += " ".join(page_number_btns)
    return html_str


def grid(db, request: tornado.httputil.HTTPServerRequest, query,
         row_render=default_row_render,
         header_render=default_header_render,
         foot_render=default_foot_render,
         order_by=None,
         paginate=20):
    page_index = 0
    if request.query_arguments.page_index and request.query_arguments.page_index.isdigit():
        page_index = int(request.query_arguments.page_index)

    all_count = db(query).count()
    db_rows = db(query).select(limitby=(paginate * page_index, (page_index + 1) * paginate), orderby=order_by)

    table_body_rows_html_content = ""
    for r in db_rows:
        table_body_rows_html_content += row_render(r, db_rows.colnames_fields)

    table_html_content = f"<div>" \
                         f"  <div>" \
                         f"    <table class='data-grid table'>" \
                         f"      <thead>{header_render(db_rows.colnames_fields)}</thead>" \
                         f"      <tbody>{table_body_rows_html_content}</tbody>" \
                         f"    </table>" \
                         f"  </div>" \
                         f"  <div class='page-numbers-container'>{foot_render(request, page_index, paginate, all_count)}</div>" \
                         f"</div>"

    return table_html_content