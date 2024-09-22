class Job:
  def __init__(self, j_id, name, pay):
    self.j_id = j_id
    self.name = name
    self.pay = pay

class Worker:
  def __init__(self, w_id, job_id, b_id, fullname, employment_date, payinfo):
    self.w_id = w_id
    self.job_id = job_id
    self.b_id = b_id
    self.fullname = fullname
    self.employment_date = employment_date
    self.payinfo = payinfo