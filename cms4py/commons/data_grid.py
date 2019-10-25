from .url import URL


def default_row_render(context, row, fields):
    html_str = "<tr>"
    for f in fields:
        html_str += f"<td>{row[f]}</td>"
    html_str += "</tr>"
    return html_str


def default_header_render(context, fields):
    html_str = "<tr>"
    for f in fields:
        html_str += f"<th>{context.locale.translate(f)}</th>"
    html_str += "</tr>"
    return html_str


def default_foot_render(context, current_page_index, paginate, all_count):
    request = context.request

    def create_link(page_index, label=None, active=False):
        return f"<li class=\"page-item {'active' if active else ''}\">" \
               f"  <a class=\"btn-page-number page-link\" href='{URL(request.path, vars=dict(page_index=page_index))}'>{(page_index + 1) if not label else label}</a>" \
               f"</li>"

    last_page_index = int(all_count / paginate)
    html_str = ""
    if last_page_index > 0:
        page_number_btns = [create_link(current_page_index, active=True)]
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


async def grid(
        context,
        query,
        fields=None,
        order_by=None,
        paginate=20,
        row_render=default_row_render,
        header_render=default_header_render,
        foot_render=default_foot_render
):
    request = context.request
    db = context.db
    page_index = int(context.get_query_argument("page_index", "0"))

    all_count = await db(query).count()
    if fields:
        db_rows = await db(query).select(
            *fields,
            limitby=(paginate * page_index, (page_index + 1) * paginate),
            orderby=order_by
        )
    else:
        db_rows = await db(query).select(
            limitby=(paginate * page_index, (page_index + 1) * paginate),
            orderby=order_by
        )

    table_body_rows_html_content = ""
    for r in db_rows:
        table_body_rows_html_content += row_render(context, r, db_rows.field_names)

    table_html_content = f"<div>" \
                         f"  <div>" \
                         f"    <table class='data-grid table'>" \
                         f"      <thead>{header_render(context, db_rows.field_names)}</thead>" \
                         f"      <tbody>{table_body_rows_html_content}</tbody>" \
                         f"    </table>" \
                         f"  </div>" \
                         f"  <div class='page-numbers-container'>" \
                         f"    <nav>" \
                         f"      <ul class='pagination'>" \
                         f"        {foot_render(context, page_index, paginate, all_count)}" \
                         f"      </ul>" \
                         f"    </nav>" \
                         f"  </div>" \
                         f"</div>"

    return table_html_content
