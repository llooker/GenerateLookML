include: "order_items_autogen.view.lkml"
view: order_items {
  extends: [order_items_autogen]

  ## Redefine dimensions to give it more properties or change calculations
  dimension: id { primary_key: yes}

  dimension: user_id {hidden: yes}

  ## Add new dimensions or measures in the extended view
  measure: count { type: count }

}
