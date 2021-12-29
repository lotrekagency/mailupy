Quickstart
==========

.. toctree::
   :maxdepth: 2
   :caption: Contents:

First of all, import Mailupy and instantiate the client::

    >>> from mailupy import Mailupy

    >>> client = Mailupy(
      'm00000',
      'm@1lUPf4k3',
      '8123dbff-d12c-4e3d-a55e-23a8c5a303f8',
      '16cadddf-a145-45db-9347-a5ab51ac223d'
    )

The client will login automatically to MailUp.
After it you can start use the client for:
  - Getting information about fields, groups...

    >>> for field in client.get_fields():
    ...     print (field)
    {'Description': 'compleanno', 'Id': 27}
    {'Description': 'idtuttiprodottiacquistati', 'Id': 26}
    {'Description': 'totalefatturatoultimi30gg', 'Id': 25}
    {'Description': 'totalefatturatoultimi12mesi', 'Id': 24}
    {'Description': 'totalefatturato', 'Id': 23}
    {'Description': 'idcarrelloabbandonato', 'Id': 22}
    {'Description': 'totalecarrelloabbandonato', 'Id': 21}
    {'Description': 'datacarrelloabbandonato', 'Id': 20}
    {'Description': 'idultimoordinespedito', 'Id': 19}
    {'Description': 'dataultimoordinespedito', 'Id': 18}
    {'Description': 'idcategorieultimoordine', 'Id': 17}
    {'Description': 'idprodottiultimoordine', 'Id': 16}
    {'Description': 'totaleultimoordine', 'Id': 15}
    {'Description': 'dataultimoordine', 'Id': 14}
    {'Description': 'idultimoordine', 'Id': 13}
    {'Description': 'idcliente', 'Id': 12}
    {'Description': 'telefono', 'Id': 11}
    {'Description': 'fax', 'Id': 10}
    {'Description': 'indirizzo', 'Id': 9}
    {'Description': 'paese', 'Id': 8}

    >>> for group in client.get_groups_from_list(1):
    ...     print (group)
    {'Count': None, 'Deletable': True, 'Name': 'Gruppo', 'Notes': '', 'idGroup': 7, 'idList': 1}
    {'Count': None, 'Deletable': False, 'Name': 'TEST', 'Notes': 'Gruppo per invii di test', 'idGroup': 6, 'idList': 1}

  - Getting recipients from lists using Ordering and Filtering
    `(Mailup Documentation) <http://help.mailup.com/display/mailupapi/Paging+and+filtering>`__

    >>> for group in client.get_groups_from_list(
    ...   1, filter_by='Name.Contains(\'Gruppo\')',
    ...   order_by=['Name asc', 'idGroup desc']):
    ...   print(group)
    {'Count': None, 'Deletable': True, 'Name': 'Gruppo', 'Notes': 'QWERTYUIOP', 'idGroup': 9, 'idList': 1}

    >>> for recipient in client.get_subscribed_recipients_from_list(
    ...   1, filter_by='Email.Contains(\'lotrek\')',
    ...   order_by=['Email desc']):
    ...   print(recipient['Email'])
    edoardo.grassi+7@lotrek.it
    edoardo.grassi+111@lotrek.it
    edoardo.grassi+10@lotrek.it
    edoardo.grassi@lotrek.it

  - Getting a subscribed recipient from a list

    >>> client.get_subscribed_recipient_from_list(1, 'edoardo.grassi@lotrek.it')
    {
      'Fields': [
        {'Description': 'nome', 'Id': 1, 'Value': ''},
        {'Description': 'cognome', 'Id': 2, 'Value': ''},
        {'Description': 'azienda', 'Id': 3, 'Value': ''},
        {'Description': 'città', 'Id': 4, 'Value': ''},
        {'Description': 'provincia', 'Id': 5, 'Value': ''},
        {'Description': 'cap', 'Id': 6, 'Value': ''},
        {'Description': 'regione', 'Id': 7, 'Value': ''},
        {'Description': 'paese', 'Id': 8, 'Value': ''},
        {'Description': 'indirizzo', 'Id': 9, 'Value': ''},
        {'Description': 'fax', 'Id': 10, 'Value': ''},
        {'Description': 'telefono', 'Id': 11, 'Value': ''},
        {'Description': 'IDCliente', 'Id': 12, 'Value': ''},
        {'Description': 'IDUltimoOrdine', 'Id': 13, 'Value': ''},
        {'Description': 'DataUltimoOrdine', 'Id': 14, 'Value': ''},
        {'Description': 'TotaleUltimoOrdine', 'Id': 15, 'Value': ''},
        {'Description': 'IDProdottiUltimoOrdine', 'Id': 16, 'Value': ''},
        {'Description': 'IDCategorieUltimoOrdine', 'Id': 17, 'Value': ''},
        {'Description': 'DataUltimoOrdineSpedito', 'Id': 18, 'Value': ''},
        {'Description': 'IDUltimoOrdineSpedito', 'Id': 19, 'Value': ''},
        {'Description': 'DataCarrelloAbbandonato', 'Id': 20, 'Value': ''},
        {'Description': 'TotaleCarrelloAbbandonato', 'Id': 21, 'Value': ''},
        {'Description': 'IDCarrelloAbbandonato', 'Id': 22, 'Value': ''},
        {'Description': 'TotaleFatturato', 'Id': 23, 'Value': ''},
        {'Description': 'TotaleFatturatoUltimi12Mesi', 'Id': 24, 'Value': ''},
        {'Description': 'TotaleFatturatoUltimi30gg', 'Id': 25, 'Value': ''},
        {'Description': 'IDTuttiProdottiAcquistati', 'Id': 26, 'Value': ''},
        {'Description': 'Compleanno', 'Id': 27, 'Value': ''}
      ],
      'Name': 'edoardo.grassi@lotrek.it',
      'idRecipient': 14,
      'Email': 'edoardo.grassi@lotrek.it',
      'MobileNumber': None,
      'MobilePrefix': None
    }

  - Subscribe/Unsubscribe recipient to/from lists

    >>> recipient_id = client.subscribe_to_list(1, 'Andrea Stagi', 'stagi.andrea@gmail.com')
    >>> client.unsubscribe_from_list(1, recipient_id)
    True
