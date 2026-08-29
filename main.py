from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.core.window import Window  # <-- Diperlukan untuk mendeteksi tombol back Android

# --- 1. MODEL OBJEK DATA ---
class ItemModel:
    def __init__(self, item_id, item_code, item_name, original_price, discounted_price, quantity, subtotal):
        self.item_id = item_id
        self.item_code = item_code
        self.item_name = item_name
        self.original_price = original_price
        self.discounted_price = discounted_price
        self.quantity = quantity
        self.subtotal = subtotal

    def to_dict(self):
        return {
            'item_id': self.item_id,
            'item_code': self.item_code,
            'item_name': self.item_name,
            'original_price': self.original_price,
            'discounted_price': self.discounted_price,
            'quantity': self.quantity,
            'subtotal': self.subtotal
        }


# --- 2. TAMPILAN ANTARMUKA (KV LANGUAGE) ---
KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<HeaderWidget>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(55)
    padding: [dp(10), dp(5)]
    spacing: dp(5)
    canvas.before:
        Color:
            rgba: get_color_from_hex('#00BCD4')
        Rectangle:
            pos: self.pos
            size: self.width/2, self.height
        Color:
            rgba: get_color_from_hex('#7C4DFF')
        Rectangle:
            pos: self.x + self.width/2, self.y
            size: self.width/2, self.height

    Button:
        text: '[M]'
        font_size: '14sp'
        size_hint_x: 0.12
        size_hint_y: 1.0
        background_color: 0,0,0,0
        color: 1,1,1,1
        bold: True

    Widget:
        size_hint_x: 0.15

    Button:
        text: 'POS 1'
        size_hint_x: 0.4
        size_hint_y: 0.8
        pos_hint: {'center_y': 0.5}
        background_color: 0,0,0,0
        canvas.before:
            Color:
                rgba: get_color_from_hex('#000000')
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20),]
        color: get_color_from_hex('#FFFFFF')
        bold: True

    Widget:
        size_hint_x: 1

    BoxLayout:
        size_hint_x: 0.33
        size_hint_y: 1.0
        spacing: dp(5)
        Label:
            text: 'TOKO HUMAIRA'
            font_size: '10sp'
            color: get_color_from_hex('#FFFFFF')
            halign: 'right'
            size_hint_x: 0.7
            text_size: self.size
            valign: 'center'
        Button:
            text: '[USER]'
            font_size: '9sp'
            size_hint_x: 0.3
            background_color: 0,0,0,0
            color: get_color_from_hex('#FFFFFF')

<QuantityControl>:
    size_hint_x: 0.25  # <-- Sudah dikecilkan agar angka rupiah tidak terpotong
    size_hint_y: 0.8
    pos_hint: {'center_y': 0.5}
    spacing: dp(1)
    padding: [dp(1), dp(0)]
    canvas.before:
        Color:
            rgba: get_color_from_hex('#FFFFFF')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12),]
            
    Button:
        text: '-'
        size_hint_x: 0.2
        size_hint_y: 1.0
        background_color: 0,0,0,0
        color: get_color_from_hex('#000000')
        bold: True
        on_release: root.update_qty(-1)
    Label:
        text: str(root.quantity)
        color: get_color_from_hex('#D32F2F')
        bold: True
        font_size: '13sp'
        size_hint_x: 0.3
        size_hint_y: 1.0
        halign: 'center'
        valign: 'center'
    Button:
        text: '+'
        size_hint_x: 0.2
        size_hint_y: 1.0
        background_color: 0,0,0,0
        color: get_color_from_hex('#000000')
        bold: True
        on_release: root.update_qty(1)
    Button:
        text: '+10'
        font_size: '8sp'
        size_hint_x: 0.3
        size_hint_y: 1.0
        background_color: 0,0,0,0
        color: get_color_from_hex('#000000')
        bold: True
        on_release: root.update_qty(10)

<CartItemWidget>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(75)
    padding: dp(6)
    spacing: dp(4)
    canvas.before:
        Color:
            rgba: get_color_from_hex('#E0F7FA')
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12),]

    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.40
        size_hint_y: 1.0
        Label:
            text: root.item_code
            font_size: '10sp'
            color: get_color_from_hex('#757575')
            halign: 'left'
            text_size: self.size
        Label:
            text: root.item_name
            font_size: '11sp'
            bold: True
            color: get_color_from_hex('#212121')
            halign: 'left'
            text_size: self.size
        BoxLayout:
            size_hint_y: 1.0
            spacing: dp(4)
            Label:
                text: root.original_price
                font_size: '9sp'
                color: get_color_from_hex('#757575')
                strikethrough: True
                halign: 'left'
                text_size: self.size
            Label:
                text: root.discounted_price
                font_size: '11sp'
                bold: True
                color: get_color_from_hex('#D32F2F')
                halign: 'left'
                text_size: self.size

    QuantityControl:
        quantity: root.quantity
        item_id: root.item_id

    BoxLayout:
        orientation: 'horizontal'
        size_hint_x: 0.35  # <-- Lebar subtotal diperluas agar aman dari potongan
        size_hint_y: 1.0
        spacing: dp(2)
        Label:
            text: root.subtotal
            font_size: '10sp'
            bold: True
            color: get_color_from_hex('#212121')
            halign: 'right'
            valign: 'center'
            size_hint_x: 0.80
            text_size: self.size
        Button:
            text: 'X'
            font_size: '11sp'
            size_hint_x: 0.20
            size_hint_y: 1.0
            background_color: 0,0,0,0
            color: get_color_from_hex('#F44336')
            bold: True
            on_release: root.delete_item()

<FooterWidget>:
    size_hint_y: None
    height: dp(55)
    canvas.before:
        Color:
            rgba: get_color_from_hex('#F44336')
        Rectangle:
            pos: self.pos
            size: self.size
    padding: dp(8)
    spacing: dp(5)
    
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.28
        size_hint_y: 1.0
        Label:
            text: 'DISKON'
            color: get_color_from_hex('#FFFFFF')
            font_size: '10sp'
            bold: True
            halign: 'left'
            text_size: self.size
        Label:
            text: 'Rp50.000'
            color: get_color_from_hex('#FFFFFF')
            font_size: '12sp'
            bold: True
            halign: 'left'
            text_size: self.size

    Button:
        text: 'BAYAR CASH'
        size_hint_x: 0.36
        size_hint_y: 0.85
        pos_hint: {'center_y': 0.5}
        background_color: 0,0,0,0
        color: get_color_from_hex('#F44336')
        bold: True
        font_size: '12sp'
        canvas.before:
            Color:
                rgba: get_color_from_hex('#FFFFFF')
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(15),]

    BoxLayout:
        orientation: 'vertical'
        size_hint_x: 0.36
        size_hint_y: 1.0
        Label:
            text: 'TOTAL HARGA'
            color: get_color_from_hex('#FFFFFF')
            font_size: '9sp'
            halign: 'right'
            text_size: self.size
        Label:
            text: 'Rp2.500.000'
            color: get_color_from_hex('#FFFFFF')
            font_size: '14sp'
            bold: True
            halign: 'right'
            text_size: self.size

<MainScreen>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: get_color_from_hex('#F5F5F5')
        Rectangle:
            pos: self.pos
            size: self.size

    HeaderWidget:

    BoxLayout:
        orientation: 'vertical'
        size_hint: (1.0, 1.0)
        padding: dp(10)
        spacing: dp(8)
        
        BoxLayout:
            size_hint_y: None
            height: dp(28)
            Label:
                text: 'Selasa, 18 Agustus 2026, 17:40 WIB'
                color: get_color_from_hex('#757575')
                font_size: '10sp'
                size_hint_x: 0.6
                halign: 'left'
                text_size: self.size
            Button:
                text: 'TAMBAH DISKON'
                size_hint_x: 0.4
                size_hint_y: 1.0
                background_color: 0,0,0,0
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#F44336')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(10),]
                color: get_color_from_hex('#FFFFFF')
                font_size: '10sp'
                bold: True

        Label:
            text: 'ID TRANS : HA0001'
            color: get_color_from_hex('#212121')
            bold: True
            font_size: '12sp'
            size_hint_y: None
            height: dp(18)
            halign: 'left'
            text_size: self.size

        BoxLayout:
            size_hint_y: None
            height: dp(38)
            spacing: dp(5)
            BoxLayout:
                size_hint_x: 0.50
                size_hint_y: 1.0
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#FFFFFF')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(15),]
                padding: [dp(8), dp(0)]
                TextInput:
                    hint_text: 'CARI BARANG...'
                    background_normal: ''
                    background_active: ''
                    multiline: False
                    size_hint: (1.0, 1.0)
                    pos_hint: {'center_y': 0.5}
            Button:
                text: 'SEARCH'
                size_hint_x: 0.25
                size_hint_y: 1.0
                background_color: 0,0,0,0
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#B3E5FC')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(15),]
                color: get_color_from_hex('#212121')
                font_size: '11sp'
                bold: True
            Button:
                text: '+ BARU'
                size_hint_x: 0.25
                size_hint_y: 1.0
                background_color: 0,0,0,0
                canvas.before:
                    Color:
                        rgba: get_color_from_hex('#FF9800')
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(15),]
                color: get_color_from_hex('#FFFFFF')
                bold: True
                font_size: '10sp'

        RecycleView:
            viewclass: 'CartItemWidget'
            data: app.cart_data
            size_hint: (1.0, 1.0)
            RecycleBoxLayout:
                default_size: None, dp(80)
                default_size_hint: (1.0, None)
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                spacing: dp(8)

    FooterWidget:
'''


# --- 3. KELAS LOGIKA & WIDGET ---
class HeaderWidget(BoxLayout):
    pass

class FooterWidget(BoxLayout):
    pass

class QuantityControl(BoxLayout):
    quantity = NumericProperty(1)
    item_id = StringProperty('')

    def update_qty(self, val):
        self.quantity = max(1, self.quantity + val)
        app = App.get_running_app()
        app.update_item_quantity(self.item_id, self.quantity)

class CartItemWidget(RecycleDataViewBehavior, BoxLayout):
    item_code = StringProperty('')
    item_name = StringProperty('')
    original_price = StringProperty('')
    discounted_price = StringProperty('')
    quantity = NumericProperty(1)
    subtotal = StringProperty('')
    item_id = StringProperty('')

    def delete_item(self):
        app = App.get_running_app()
        app.remove_item(self.item_id)

    def refresh_view_attrs(self, rv, index, data):
        self.item_code = data.get('item_code', '')
        self.item_name = data.get('item_name', '')
        self.original_price = data.get('original_price', '')
        self.discounted_price = data.get('discounted_price', '')
        self.quantity = data.get('quantity', 1)
        self.subtotal = data.get('subtotal', '')
        self.item_id = data.get('item_id', '')
        return super().refresh_view_attrs(rv, index, data)

class MainScreen(BoxLayout):
    pass


# --- 4. APLIKASI UTAMA ---
class POSApp(App):
    cart_data = ListProperty([])

    def build(self):
        # Mendaftarkan event tombol Back Android agar bisa kembali / keluar ke Pydroid
        Window.bind(on_keyboard=self._on_keyboard)

        Builder.load_string(KV)
        
        raw_items = [
            ItemModel('1', '1554980', 'KOPI KAPAL API 23GR', '', 'Rp2.000', 5, 'Rp2.500.000'),
            ItemModel('2', '1554980', 'INDOMIE SOTO 70G', 'Rp250.000', 'Rp200.000', 15, 'Rp2.500.000'),
            ItemModel('3', '1554980', 'KOPI KAPAL API 23GR', '', 'Rp2.000', 5, 'Rp17.000')
        ]
        
        self.cart_data = [item.to_dict() for item in raw_items]
        return MainScreen()

    def _on_keyboard(self, window, key, *args):
        # Tombol back di Android / Escape di keyboard komputer bernilai 27
        if key == 27:
            self.stop()  # Menutup aplikasi Kivy dan kembali ke Pydroid 3
            return True
        return False

    def update_item_quantity(self, item_id, new_qty):
        for item in self.cart_data:
            if item['item_id'] == item_id:
                item['quantity'] = new_qty
                break

    def remove_item(self, item_id):
        self.cart_data = [item for item in self.cart_data if item['item_id'] != item_id]


if __name__ == '__main__':
    POSApp().run()

