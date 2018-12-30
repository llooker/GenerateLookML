view: order_items_autogen {
sql_table_name: PUBLIC.ORDER_ITEMS ;;

dimension_group: created_at {
  timeframes: [raw
  ,year
  ,quarter
  ,month
  ,week
  ,date
  ,day_of_week
  ,month_name]
  type: time
  sql: ${TABLE}.CREATED_AT ;;
}

  
dimension_group: delivered_at {
  timeframes: [raw
  ,year
  ,quarter
  ,month
  ,week
  ,date
  ,day_of_week
  ,month_name]
  type: time
  sql: ${TABLE}.DELIVERED_AT ;;
}

  
dimension: id {
  sql: ${TABLE}.ID ;;
  type: number
}

  
dimension: inventory_item_id {
  sql: ${TABLE}.INVENTORY_ITEM_ID ;;
  type: number
}

  
dimension: order_id {
  sql: ${TABLE}.ORDER_ID ;;
  type: number
}

  
dimension_group: returned_at {
  timeframes: [raw
  ,year
  ,quarter
  ,month
  ,week
  ,date
  ,day_of_week
  ,month_name]
  type: time
  sql: ${TABLE}.RETURNED_AT ;;
}

  
dimension: sale_price {
  sql: ${TABLE}.SALE_PRICE ;;
  type: number
}

  
dimension_group: shipped_at {
  timeframes: [raw
  ,year
  ,quarter
  ,month
  ,week
  ,date
  ,day_of_week
  ,month_name]
  type: time
  sql: ${TABLE}.SHIPPED_AT ;;
}

  
dimension: status {
  sql: ${TABLE}.STATUS ;;
  type: string
}

  
dimension: user_id {
  sql: ${TABLE}.USER_ID ;;
  type: number
}

}
