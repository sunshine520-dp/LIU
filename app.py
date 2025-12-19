import streamlit as st
import pandas as pd
import plotly.express as px

# 设置页面标题
st.set_page_config(page_title="数字化转型指数查询与可视化", page_icon="📊", layout="wide")

# 页面标题
st.title("📊 数字化转型指数查询与可视化")

# 实现数据加载功能
@st.cache_data

def load_data():
    """加载Excel数据"""
    try:
        df = pd.read_excel('历年数字化转型指数汇总.xlsx')
        # 处理股票代码，确保为字符串格式，保留前导零
        df['股票代码'] = df['股票代码'].astype(str).str.zfill(6)
        return df
    except Exception as e:
        st.error(f"数据加载失败: {e}")
        return pd.DataFrame()

# 加载数据
df = load_data()

if not df.empty:
    # 侧边栏查询设置
    st.sidebar.header("🔍 查询设置")
    
    # 股票代码选择器
    stock_codes = sorted(df['股票代码'].unique())
    selected_stock = st.sidebar.selectbox("选择股票代码", stock_codes)
    
    # 年份选择器
    years = sorted(df['年份'].unique())
    selected_year = st.sidebar.selectbox("选择年份", years)
    
    # 查询按钮
    if st.sidebar.button("查询"):
        # 根据选择的股票代码和年份过滤数据
        filtered_data = df[(df['股票代码'] == selected_stock) & (df['年份'] == selected_year)]
        
        if not filtered_data.empty:
            st.success(f"查询结果：{filtered_data['企业名称'].values[0]} ({selected_stock}) - {selected_year}年")
            st.metric("数字化转型指数", filtered_data['数字化转型指数'].values[0])
        else:
            st.warning("未找到匹配的数据")
    
    # 显示该股票的历年数字化转型指数折线图
    st.header(f"📈 {selected_stock}历年数字化转型指数趋势")
    stock_data = df[df['股票代码'] == selected_stock].sort_values('年份')
    
    if not stock_data.empty:
        fig = px.line(stock_data, x='年份', y='数字化转型指数', 
                     title=f"{stock_data['企业名称'].values[0]} ({selected_stock})历年数字化转型指数",
                     markers=True, 
                     labels={'数字化转型指数': '指数值', '年份': '年份'})
        fig.update_layout(xaxis_title="年份", yaxis_title="数字化转型指数", 
                         title_x=0.5, hovermode="x unified")
        st.plotly_chart(fig, width='stretch')
        
        # 显示数据表格
        st.subheader("详细数据")
        st.dataframe(stock_data[['年份', '数字化转型指数']], width='stretch')
    else:
        st.info("暂无该股票的历史数据")
    
    # 显示数据统计信息
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 数据统计")
    st.sidebar.write(f"总企业数: {df['企业名称'].nunique()}")
    st.sidebar.write(f"总股票数: {df['股票代码'].nunique()}")
    st.sidebar.write(f"年份范围: {min(years)} - {max(years)}")
    st.sidebar.write(f"数据总量: {len(df)} 条")
else:
    st.error("未加载到数据，请检查Excel文件是否存在")