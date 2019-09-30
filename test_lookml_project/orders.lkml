view: orders {
  sql_table_name: analytics.orders ;;

  dimension: order_id {
    primary_key: yes
    type: number
    sql: ${TABLE}.order_id ;;
  }

  dimension: amount {
    type: number
    value_format_name: usd
  }
}
