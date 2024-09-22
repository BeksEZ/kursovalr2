class Contract:
  def __init__(self, contract_id, client_id, b_id, date_signed, date_closed, contract_sum, status):
    self.contract_id = contract_id
    self.client_id = client_id
    self.b_id = b_id
    self.date_signed = date_signed
    self.date_closed = date_closed
    self.contract_sum = contract_sum
    self.status = status