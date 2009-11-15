"""
A flexible generic data model for cabinet industry.

   * provide for easy data entry from manufacturers catalogs   * present information in a way that minimizes erroneous selections
      * enumerate types of options for a particular artifact
      * enumerate all options of a particular type
      * show valid options based on context of current selections
   * validate selections
      * rules for 
      * constraints
   * model relationships?
   
Data Example
    * the kingston door comes in maple, cherry and lyptus
       * the cherry stain are chocolate, espresso and coffee
       * the maple stains are coffe, taupe and olive
       * the lyptus stains are all of the above
       * also support paint options of red white or blue
       * stained doors support glazes of X Y and Z
       * special   finishoptions include speckling, distressing and dodging    

    results in - 
      - an item_type of 'door'
      - an item of type 'door' with value 'kingston'
      - attribute_type of 'stain'
      - and attribute of type 'stain' with value '



"""
