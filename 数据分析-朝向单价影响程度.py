import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Bar

def draw(data):
    c = (
        Bar(init_opts=opts.InitOpts(
            width='1800px',
            height='800px',
            js_host="./",
        ))
        .add_xaxis(data.index.tolist())
        .add_yaxis("是", data['是'].tolist(), stack="stack1", category_gap="50%")
        .add_yaxis("否", data['否'].tolist(), stack="stack1", category_gap="50%")
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            title_opts=opts.TitleOpts(title="南昌红谷滩二手房朝向影响"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical")
        )
        .render('分析图表/' + "南昌红谷滩二手房朝向影响.html")
    )

def has_desired_orientation(orientation):
    desired_orientations = ['南', '东', '东南']
    return any(direction in orientation for direction in desired_orientations)

def clean_price(price_str):
    # 提取数字部分，并转换为浮点数
    try:
        return float(''.join(filter(str.isdigit, price_str)))
    except ValueError:
        return None 
    
def read_csv():
    file = 'honggutan.csv'
    data = pd.read_csv('./爬取结果/' + file, encoding='gb18030', header=None)
    data.columns = ['名称', '小区名', '位置', '房间类型', '面积', '朝向', '装修', '楼层', '年份', '楼况', '关注人数', '发布时间', '总价', '单价', '标签']
    data['是否东南朝向'] = data['朝向'].apply(lambda x: '是' if has_desired_orientation(x) else '否')
    data['单价'] = data['单价'].apply(clean_price)
    a = pd.pivot_table(data, values='单价', index=['小区名'], columns=['是否东南朝向'], aggfunc='mean', fill_value=0)
    a.to_csv('朝向影响单价.csv', encoding='utf-8')
    draw(a)


if __name__ == '__main__':
    read_csv()
