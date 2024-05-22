from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.pin import *
from pywebio_battery import popup_input, confirm


# bagian BinarySearchTree
class Barang:
    def __init__(self, sku, nama_barang, harga_satuan, jumlah_stok):
        self.sku = sku
        self.nama_barang = nama_barang
        self.harga_satuan = harga_satuan
        self.jumlah_stok = jumlah_stok


class Node:
    def __init__(self, barang):
        self.barang = barang
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, barang):
        new_node = Node(barang)
        if self.root is None:
            self.root = new_node
            return True
        else:
            temp = self.root
            while True:
                if barang.sku < temp.barang.sku:
                    if temp.left is None:
                        temp.left = new_node
                        return True
                    temp = temp.left
                elif barang.sku > temp.barang.sku:
                    if temp.right is None:
                        temp.right = new_node
                        return True
                    temp = temp.right
                else:
                    return False

    def collect_data(self, node, data=[]):
        if node is not None:
            self.collect_data(node.left, data)
            data.append(
                [
                    node.barang.sku,
                    node.barang.nama_barang,
                    node.barang.harga_satuan,
                    node.barang.jumlah_stok,
                ]
            )
            self.collect_data(node.right, data)
        return data

    def print_bst(self):
        data = self.collect_data(self.root)
        return data

    # untuk mengecek apakah no sku sudah ada di bst?
    def contains(self, sku):
        temp = self.root
        while temp is not None:
            if sku < temp.barang.sku:
                temp = temp.left
            elif sku > temp.barang.sku:
                temp = temp.right
            else:
                return True
        return False

    def find_node(self, sku):
        temp = self.root
        while temp is not None:
            if sku < temp.barang.sku:
                temp = temp.left
            elif sku > temp.barang.sku:
                temp = temp.right
            else:
                return temp.barang
        return None


# objek bst
bst = BinarySearchTree()


def stok_barang():
    # popup_input
    clear()
    while True:
        sbmn_stok_barang = radio(
            "Menu yang tersedia",
            [
                "1. Input Data Stok Barang",
                "2. Restok Barang",
                "3. Kembali ke menu utama",
            ],
        )
        if sbmn_stok_barang == "1. Input Data Stok Barang":
            with use_scope("message", clear=True):
                pinput_stok_barang = popup_input(
                    [
                        put_input("sku", label="Masukkan No.sku", type=NUMBER),
                        put_input(
                            "nama_barang", label="Masukkan nama barang", type=TEXT
                        ),
                        put_input(
                            "harga_satuan", label="Masukkan harga satuan", type=NUMBER
                        ),
                        put_input(
                            "jumlah_stok", label="Masukkan jumlah stok", type=NUMBER
                        ),
                    ],
                    title="input data stok barang",
                )

                if pinput_stok_barang["sku"] < 1000 or pinput_stok_barang["sku"] > 9999:
                    put_info("No.sku tidak valid. Harap masukkan nomor 4 digit")
                else:
                    if bst.contains(pinput_stok_barang["sku"]):
                        put_text("sku tersebut sudah ada")
                    else:
                        barang = Barang(
                            pinput_stok_barang["sku"],
                            pinput_stok_barang["nama_barang"],
                            pinput_stok_barang["harga_satuan"],
                            pinput_stok_barang["jumlah_stok"],
                        )
                        if bst.insert(barang):
                            put_info("Barang berhasil ditambahkan.")
        elif sbmn_stok_barang == "2. Restok Barang":
            with use_scope("message", clear=True):
                data = bst.print_bst()
                pinput_restok_barang = popup_input(
                    [
                        put_input(
                            "jmh_stok_baru",
                            label="Masukkan No.sku barang yang akan di restok : ",
                            type=NUMBER,
                        ),
                        put_table(
                            data,
                            header=[
                                "No. SKU",
                                "Nama Barang",
                                "Harga Satuan",
                                "Jumlah Stok",
                            ],
                        ),
                    ],
                    title="Restok barang",
                )
                no_sku_barang = bst.find_node(pinput_restok_barang["jmh_stok_baru"])
                if bst.contains(pinput_restok_barang["jmh_stok_baru"]) is None:
                    put_info(f"Barang dengan No.sku {no_sku_barang} tidak ditemukan.")
                else:
                    stok_baru = popup_input(
                        [
                            put_input(
                                "stok_baru",
                                label="Masukkan jumlah stok tambahan",
                                type=NUMBER,
                            )
                        ]
                    )
                    no_sku_barang.jumlah_stok += stok_baru["stok_baru"]
                    put_info(
                        f"Stok barang dengan No.sku {no_sku_barang}  berhasil ditambahkan\njumlah stok sekarang : {no_sku_barang.jumlah_stok}"
                    )
        elif sbmn_stok_barang == "3. Kembali ke menu utama":
            main_sistem()
            break


# ini adalah bagian menu dari SITORASI(Sistem Informasi Stok dan Transaksi)
def main_sistem():
    clear()
    while True:
        put_markdown("### SITORSI")
        put_markdown("### Sistem Informasi Stok dan Transaksi")
        mn_stok_barang = radio(
            "Menu yang tersedia",
            [
                "1. Kelola Stok Barang",
                "2. Kelola Transaksi Konsumen",
                "3. Keluar Program",
            ],
        )
        if mn_stok_barang == "1. Kelola Stok Barang":
            stok_barang()


start_server(main_sistem, port=8080)
