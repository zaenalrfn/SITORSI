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
        data = self.collect_data(self.root, [])
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

# bagian untuk menyimpan data transaksi baru
data_transaksi_baru = []


# bagian sorted data descending
def selection_sort(transaksi):
    for i in range(len(transaksi) - 1):
        max_index = i
        for j in range(i + 1, len(transaksi)):
            if transaksi[j][3] > transaksi[max_index][3]:
                max_index = j
        if i != max_index:
            transaksi[i], transaksi[max_index] = (
                transaksi[max_index],
                transaksi[i],
            )
    return transaksi


# untuk menampilkan data transaksi
def print_data_transaksi(data):
    head = ["Nama Konsumen", "No. SKU", "Jumlah Beli", "Subtotal"]
    put_table([head] + data)


# untuk menampilkan data barang
def print_data_barang(data):
    head = ["No. SKU", "Nama", "Harga Satuan", "Jumlah stok"]
    put_table([head] + data)


# untuk menampilkan data konsumen
def print_data_bedasarkan_subtotal():
    sorted_list = selection_sort(data_transaksi_baru)
    print_data_transaksi(sorted_list)


def stok_barang():
    # popup_input
    with use_scope("message", clear=True):
        while True:
            sbmn_stok_barang = radio(
                "Menu yang tersedia",
                [
                    "1. Input Data Stok Barang",
                    "2. Restok Barang",
                    "3. Lihat Data Barang",
                    "0. Kembali ke menu utama",
                ],
            )
            if sbmn_stok_barang == "1. Input Data Stok Barang":
                with use_scope("message", clear=True):
                    pinput_stok_barang = popup_input(
                        [
                            put_input(
                                "sku", label="Masukkan No.sku 4 digit", type=NUMBER
                            ),
                            put_input(
                                "nama_barang", label="Masukkan nama barang", type=TEXT
                            ),
                            put_input(
                                "harga_satuan",
                                label="Masukkan harga satuan",
                                type=NUMBER,
                            ),
                            put_input(
                                "jumlah_stok", label="Masukkan jumlah stok", type=NUMBER
                            ),
                        ],
                        title="input data stok barang",
                    )

                    if (
                        pinput_stok_barang["sku"] < 1000
                        or pinput_stok_barang["sku"] > 9999
                    ):
                        with use_scope("message", clear=True):
                            put_info("No.sku tidak valid. Harap masukkan nomor 4 digit")
                    else:
                        with use_scope("message", clear=True):
                            if bst.contains(pinput_stok_barang["sku"]):
                                put_info("No. SKU yang diinputkan sudah terdaftar")

                            else:
                                barang = Barang(
                                    pinput_stok_barang["sku"],
                                    pinput_stok_barang["nama_barang"],
                                    pinput_stok_barang["harga_satuan"],
                                    pinput_stok_barang["jumlah_stok"],
                                )
                                if bst.insert(barang):
                                    put_success("Barang berhasil ditambahkan.")
            elif sbmn_stok_barang == "2. Restok Barang":
                with use_scope("message", clear=True):

                    pinput_restok_barang = popup_input(
                        [
                            put_input(
                                "jmh_stok_baru",
                                label="Masukkan No.sku 4 digit barang yang akan di restok : ",
                                type=NUMBER,
                            ),
                        ],
                        title="Restok barang",
                    )
                    no_sku_barang = bst.find_node(pinput_restok_barang["jmh_stok_baru"])
                    if not bst.contains(pinput_restok_barang["jmh_stok_baru"]):
                        put_info(
                            f"Barang dengan No.sku {no_sku_barang} tidak ditemukan. Harap input data stok barang dulu!"
                        )
                    else:
                        stok_baru = popup_input(
                            [
                                put_input(
                                    "stok_baru",
                                    label="Masukkan jumlah stok tambahan",
                                    type=NUMBER,
                                )
                            ],
                            title="Tambah Stok",
                        )
                        total_stok_barang = (
                            no_sku_barang.jumlah_stok + stok_baru["stok_baru"]
                        )
                        no_sku_barang.jumlah_stok = total_stok_barang
                        put_success(
                            f"Stok barang dengan No.sku {no_sku_barang}  berhasil ditambahkan\njumlah stok sekarang : {no_sku_barang.jumlah_stok}"
                        )
            elif sbmn_stok_barang == "3. Lihat Data Barang":
                with use_scope("message", clear=True):
                    data = bst.print_bst()
                    with popup("Data barang"):
                        print_data_barang(data)
            elif sbmn_stok_barang == "0. Kembali ke menu utama":
                main_sistem()
                break


# bagian kelola transaksi konsumen
def transaksi_konsumen():
    with use_scope("message", clear=True):
        while True:
            sbmn_kelola_transaksi = radio(
                "Menu yang tersedia",
                [
                    "1. Input Data Transaksi Baru",
                    "2. Lihat Data Seluruh Transaksi Konsumen",
                    "3. Lihat Data Transaksi Berdasarkan Subtotal",
                    "0. Kembali ke menu utama",
                ],
            )
            if sbmn_kelola_transaksi == "1. Input Data Transaksi Baru":
                nama_konsumen = input("Masukkan nama konsumen", type=TEXT)
                while True:
                    no_sku = popup_input(
                        [
                            put_input(
                                "no_sku",
                                label="Masukkan No.sku 4 digit barang yang dibeli",
                                type=NUMBER,
                            )
                        ],
                        title="input No sku",
                    )
                    if bst.contains(no_sku["no_sku"]):
                        jumlah_beli = popup_input(
                            [
                                put_input(
                                    "jumlah_beli",
                                    label="Masukkan jumlah beli",
                                    type=NUMBER,
                                )
                            ],
                            title="Jumlah Beli",
                        )
                        barang = bst.find_node(no_sku["no_sku"])
                        if barang.jumlah_stok >= jumlah_beli["jumlah_beli"]:
                            with use_scope("message", clear=True):
                                barang.jumlah_stok -= jumlah_beli["jumlah_beli"]
                                sub_total = (
                                    barang.harga_satuan * jumlah_beli["jumlah_beli"]
                                )
                                data_transaksi_baru.append(
                                    [
                                        nama_konsumen,
                                        no_sku,
                                        jumlah_beli["jumlah_beli"],
                                        sub_total,
                                    ]
                                )
                                put_success(
                                    "Data Transaksi Konsumen Berhasil Diinputkan"
                                )
                                lanjut_transaksi = radio(
                                    "Apakah ingin menambahkan data pembelian untuk konsumen ini (Y/N)?",
                                    ["Y", "N"],
                                )
                                if lanjut_transaksi == "Y":
                                    continue
                                else:
                                    break
                        elif barang.jumlah_stok < jumlah_beli["jumlah_beli"]:
                            with use_scope("message", clear=True):
                                put_error(
                                    "Jumlah Stok No.SKU yang Anda beli tidak mencukupi"
                                )
                                lanjut_transaksi = radio(
                                    "Apakah ingin melanjutkan transaksi (Y/N)?",
                                    ["Y", "N"],
                                )
                                if lanjut_transaksi == "Y":
                                    continue
                                else:
                                    break
                    else:
                        with use_scope("message", clear=True):
                            put_error("No. SKU yang diinputkan belum terdaftar")
                            lanjut_transaksi = radio(
                                "Apakah ingin melanjutkan transaksi (Y/N)?", ["Y", "N"]
                            )
                            if lanjut_transaksi == "Y":
                                continue
                            else:
                                break
            elif sbmn_kelola_transaksi == "2. Lihat Data Seluruh Transaksi Konsumen":
                with use_scope("message", clear=True):
                    print_data_transaksi(data_transaksi_baru)

            elif (
                sbmn_kelola_transaksi == "3. Lihat Data Transaksi Berdasarkan Subtotal"
            ):
                # INI ADALAH BAGIAN LIHAT DATA TRANSAKSI BEDASARKAN SUBTOTAL
                with use_scope("message", clear=True):
                    print_data_bedasarkan_subtotal()

            elif sbmn_kelola_transaksi == "0. Kembali ke menu utama":
                with use_scope("message", clear=True):
                    main_sistem()
                    break


# ini adalah bagian menu dari SITORASI(Sistem Informasi Stok dan Transaksi)
def main_sistem():
    with use_scope("message", clear=True):
        while True:
            put_markdown("### SITORSI")
            put_markdown("### Sistem Informasi Stok dan Transaksi")
            mn_stok_barang = radio(
                "Menu yang tersedia",
                [
                    "1. Kelola Stok Barang",
                    "2. Kelola Transaksi Konsumen",
                    "0. Keluar Program",
                ],
            )
            if mn_stok_barang == "1. Kelola Stok Barang":
                stok_barang()
            elif mn_stok_barang == "2. Kelola Transaksi Konsumen":
                transaksi_konsumen()
            elif mn_stok_barang == "0. Keluar Program":
                with use_scope("message", clear=True):
                    put_info("Terimaksih sudah menggunakan SITORSI")
                    break


start_server(main_sistem, port=8080)
