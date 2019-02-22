## 说明

```
    // 默认搜索
    default_query = '''
    {
      allEmployees {
        totalCount
        edges {
          node {
            id
            name
            department {
              id
              name
            }
            role {
              id
              name
            }
          }
        }
      }
    }'''.strip()
```