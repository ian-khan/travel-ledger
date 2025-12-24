from travel_ledger.core.schema import Column, COLUMNS

def format_header_footer() -> tuple[str, str]:
    hrz_line = "+-" + "-+-".join(["-" * col.width for col in COLUMNS]) + "-+"
    lbl_line = "| " + " | ".join([col.format_printed_label() for col in COLUMNS]) + " |"
    return hrz_line + '\n' + lbl_line + '\n' + hrz_line, hrz_line

def format_records(records: list[tuple]) -> str:
    hrz_line = "\n+-" + "-+-".join(["-" * col.width for col in COLUMNS]) + "-+\n"

    val_lines = []
    for record in records:
        val_line = "| " + " | ".join([col.format_printed_value(val)
                                      for col, val in zip(COLUMNS, record)]) + " |"
        val_lines.append(val_line)

    return hrz_line.join(val_lines)

def format_summary(col_name: str, summed_records: list[tuple]) -> str:
    widths = [14, 14, 14]
    hrz_line = "+-" + "-+-".join(["-" * width for width in widths]) + "-+\n"
    labels = [col_name, "Amount (JPN)", "Proportion (%)"]
    lbl_line = "| " + " | ".join([label.ljust(width)
                                  for label, width in zip(labels, widths)]) + " |\n"
    all_groups_sum = sum([group_sum for _, group_sum in summed_records])
    grp_lines = []
    for group_name, group_sum in summed_records:
        entries = [group_name,
                   round(group_sum, 1),
                   0.0 if all_groups_sum == 0 else round((group_sum / all_groups_sum * 100), 1)]
        grp_line = "| " + " | ".join([str(entry)[:width].ljust(width)
                                      for entry, width in zip(entries, widths)]) + " |\n"
        grp_lines.append(grp_line)
    totals = ["Total", all_groups_sum, "100.0"]
    ttl_line = "| " + " | ".join([str(total).ljust(width)
                                  for total, width in zip(totals, widths)]) + " |\n"
    summary = hrz_line + hrz_line.join([lbl_line] + grp_lines + [ttl_line]) + hrz_line
    return summary


