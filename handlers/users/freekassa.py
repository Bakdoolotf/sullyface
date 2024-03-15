from config import config
import aiohttp,datetime,hashlib,hmac,json
from collections import OrderedDict

class FreeKassa:
    API_URL = 'https://api.freekassa.ru/v1/'
    API_ORDERS_ROUTE = 'orders'
    _nonce = 0
    def __init__(self) -> None:
        pass
    
    async def find_order_by_merchant_id(self,order_list, merchant_id):
        found_orders = []
        for order in order_list['orders']:
            print(order)
            if order['merchant_order_id'] == merchant_id:
                found_orders.append(order)
        if len(found_orders) == 0:
            return json.dumps({"status": "error", "message": f"No orders found with merchant_order_id {merchant_id}"})
        else:
            for order in found_orders:
                #return order['merchant_order_id'],order['fk_order_id'],order['amount'],order['currency'],order['email'],order['date'],order['status'],order['commission']
                return json.dumps({"status": "success", "orders": found_orders})

    async def create_payment_link(self,order_id,order_amount,currency = 'RUB', sbp=False):
            sign = hashlib.md5((f"{config('freekassa_merchant_id')}:{order_amount}:{config('freekassa_secret_word')}:{currency}:{order_id}").encode('utf-8')).hexdigest()
            text = ''
            if sbp:
                text = '&i=42'
            pay_url = f"https://pay.freekassa.ru/?m={config('freekassa_merchant_id')}&oa={order_amount}&currency={currency}&o={order_id}&s={sign}{text}"
            async with aiohttp.ClientSession() as session:
                async with session.get(pay_url) as response:
                    if response.status == 200:
                        return pay_url
                    else:
                        return ''
            
    async def get_orders(self, order_id: int = None, payment_id: str = None, order_status: int = None,
                          date_from: datetime.datetime = None, date_to: datetime.datetime = None, page: int = None):
        additional_fields = {}
        if order_id:
            additional_fields['orderId'] = order_id
        if payment_id:
            additional_fields['paymentId'] = payment_id
        if order_status:
            additional_fields['orderStatus'] = order_status
        if date_from:
            additional_fields['dateFrom'] = self._get_time_str(date_from)
        if date_to:
            additional_fields['dateFrom'] = self._get_time_str(date_to)
        if page:
            additional_fields['page'] = page
        return await self._request(self.API_ORDERS_ROUTE, additional_fields=additional_fields)
    @staticmethod
    def _get_time_str(dt: datetime.datetime):
        return dt.strftime('%Y.%m.%d %H:%M:%S')

    def _get_url(self, route, **kwargs):
        url = f'{self.API_URL}{route}'
        for key, value in kwargs.items():
            url = url.replace(f'%{key}%', value)
        return url
    
    def _get_data(self, additional_fields=dict):
        data = OrderedDict({'shopId': config('freekassa_merchant_id'), 'nonce': self._nonce})
        data.update(additional_fields)
        data.update({'signature': self._get_signature(data=data)})
        return data

    def _get_signature(self, data):
        cdata = dict(data)
        if 'amount' in cdata:
            amount = cdata['amount']
            _ = f"{round(amount % 1, 2)}"[1:4] if amount % 1 > 0 else ''
            cdata['amount'] = f"{int(amount)}{_}"
        msg = '|'.join([str(cdata.get(key)) for key in sorted(cdata.keys())])
        hash_object = hmac.new(
            key=config('freekassa_api_key').encode(),
            msg=msg.encode(),
            digestmod=hashlib.sha256
        )
        return hash_object.hexdigest()

    def _set_nonce(self):
        self._nonce = int(datetime.datetime.now().timestamp())

    async def _request(self, route, additional_fields=None, **kwargs):
        self._set_nonce()
        if additional_fields is None:
            additional_fields = {}
        async with aiohttp.ClientSession() as session:
            async with session.post(url=self._get_url(route, **kwargs), json=self._get_data(additional_fields)) as response:
                message = 'No message'
                text_json = await response.text()
                text_json = json.loads(text_json)
                if 'msg' in text_json:
                    message = text_json.get('msg')
                if 'message' in text_json:
                    message = text_json.get('message')
                if 'error' in text_json:
                    message = text_json.get('error')
                if response.status == 400:
                    print(message)
                if response.status == 401:
                    print(message)
                return text_json
