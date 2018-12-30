view: users_autogen {
sql_table_name: PUBLIC.USERS ;;

dimension: age {
  sql: ${TABLE}.AGE ;;
  type: number
}

  
dimension: city {
  sql: ${TABLE}.CITY ;;
  type: string
}

  
dimension: country {
  sql: ${TABLE}.COUNTRY ;;
  type: string
}

  
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

  
dimension: email {
  sql: ${TABLE}.EMAIL ;;
  type: string
}

  
dimension: first_name {
  sql: ${TABLE}.FIRST_NAME ;;
  type: string
}

  
dimension: gender {
  sql: ${TABLE}.GENDER ;;
  type: string
}

  
dimension: id {
  sql: ${TABLE}.ID ;;
  type: number
}

  
dimension: last_name {
  sql: ${TABLE}.LAST_NAME ;;
  type: string
}

  
dimension: latitude {
  sql: ${TABLE}.LATITUDE ;;
  type: number
}

  
dimension: longitude {
  sql: ${TABLE}.LONGITUDE ;;
  type: number
}

  
dimension: state {
  sql: ${TABLE}.STATE ;;
  type: string
}

  
dimension: traffic_source {
  sql: ${TABLE}.TRAFFIC_SOURCE ;;
  type: string
}

  
dimension: zip {
  sql: ${TABLE}.ZIP ;;
  type: string
}

}
