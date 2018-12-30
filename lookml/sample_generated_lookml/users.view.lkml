include: "users_autogen.view.lkml"
view: users {
  extends: [users_autogen]

  ## Redefine dimensions to give it more properties or change calculations
  dimension: id { primary_key: yes }

  ## Add new dimensions or measures in the extended view
  measure: count { type: count }

}
