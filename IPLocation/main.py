import tkinter.messagebox, geoip2.database, re

class FindLocation(object):
    def __init__(self):
        # 加载数据库（官网上免费数据库），数据库文件在根目录
        self.reader = geoip2.database.Reader('.\GeoLite2-City.mmdb')
        self.asn = geoip2.database.Reader('GeoLite2-ASN.mmdb')
        # 创建主窗口，即为根窗口
        self.root = tkinter.Tk(className='IP Location')
        # 创建一个输入框并设置尺寸
        self.input_ip = tkinter.Entry(self.root, width=30)
        # 创建一个回显列表
        self.display_info = tkinter.Listbox(self.root, width=50)
        # 创建一个查询结果按钮
        self.rs_btn = tkinter.Button(self.root, command=self.find_position, text='查询')

    # UI布局
    def gui_arrange(self):
        self.input_ip.pack()
        self.display_info.pack()
        self.rs_btn.pack()

    def find_position(self):
        input = self.input_ip.get()

        # 利用正则检验
        if re.search(r'\d{1,3}.\d{1,3}.\d{1,3}', input) == None:
            tkinter.messagebox.showerror('出错了', '非有效IP地址', parent=self.root)
            return

        try:
            data = self.reader.city(input)
            asn  =self.asn.asn(input)
            asnt = asn.autonomous_system_number
            asno = asn.autonomous_system_organization
            city = data.city.name
            country = data.country.name
            postal_code = data.postal.code  # 邮编
            longitude = data.location.longitude  # 经度
            latitude = data.location.latitude  # 纬度
        except geoip2.errors.AddressNotFoundError:
            tkinter.messagebox.showerror('出错了', '此IP不在数据库中', parent=self.root)
            return
        except RuntimeError as e:
            tkinter.messagebox.showerror('出错了', Exception, parent=self.root)
            return

        # 创建回显列表
        info = ['城市：' + str(city), '国家：' + str(country), '邮编：' + str(postal_code), '经度：' + str(longitude),
                '纬度：' + str(latitude),'ASN编号：' + str(asnt),'运营商：' + str(asno)]
        print(info)
        # 清空回显列表，类似于clear
        for i in range(10):
            self.display_info.insert(0, '')
        # 为回显列表赋值
        for i in range(len(info)):
            self.display_info.insert(i, info[i])


if __name__ == '__main__':
    fl = FindLocation()
    fl.gui_arrange()
    tkinter.mainloop()
