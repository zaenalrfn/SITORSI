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

    def print_bst(self, node, level=0):
        if node is not None:
            self.print_bst(node.left, level + 1)
            put_text(" " * 4 * level + "->", node.barang.sku)
            self.print_bst(node.right, level + 1)

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
            pinput_stok_barang = popup_input(
                [
                    put_input("sku", label="Masukkan sku"),
                    put_input("nama_barang", label="Masukkan nama barang"),
                    put_input("harga_satuan", label="Masukkan harga satuan"),
                    put_input("jumlah_stok", label="Masukkan jumlah stok"),
                ],
                title="input data stok barang",
            )
            if bst.contains(pinput_stok_barang["sku"]):
                clear()
                put_text("sku tersebut sudah ada")
            else:
                barang = Barang(
                    pinput_stok_barang["sku"],
                    pinput_stok_barang["nama_barang"],
                    pinput_stok_barang["harga_satuan"],
                    pinput_stok_barang["jumlah_stok"],
                )
                if bst.insert(barang):
                    clear()
                    put_text("Barang berhasil ditambahkan.")
                    bst.print_bst(bst.root)


# ini adalah bagian menu dari SITORASI(Sistem Informasi Stok dan Transaksi)
def main_sistem():
    while True:
        # put_text("SITORASI")
        # put_text("Sistem Informasi Stok dan Transaksi")
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
