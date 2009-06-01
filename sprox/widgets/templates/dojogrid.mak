<table xmlns="http://www.w3.org/1999/xhtml" xmlns:py="http://genshi.edgewall.org/"
                         dojoType="${dojoType}"
                         jsId="${jsId}"
                         id="${id}"
                         store="${jsId}_store"
                         columnReordering="${columnReordering}"
                         rowsPerPage="${rowsPerPage}"
                         model="${model}"
                         delayScroll="${delayScroll}"
                         class="${cssclass}"
                         >
    <thead>
            <tr>
                % for column in columns:
                    <th width="${column_widths.get(column, default_column_width)}" name="${headers.get(column, column)}" field="${column}">${column}</th>
                % endfor
            </tr>
    </thead>
    <div dojoType="dojox.data.QueryReadStore" jsId="${jsId}_store"  id="${jsId}_store" url="${action}"/>
</table>