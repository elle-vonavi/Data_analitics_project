# Data_analitics_project
Анализ ленты новостей мобильного приложения (учебный проект)
У нас есть мобильное приложение, позволяющее пользователям листать ленту новостей и ставить лайки понравившимся постам. Данные об активности пользователей хранятся в таблице Clickhouse "feed_actions" в следующем формате: 
- user_id: id пользователя 
- post_id: id поста action: 
- событие (просмотр или лайк) 
- time: время совершения события
- gender: пол пользователя age: возраст пользователя 
- country: страна пользователя 
- city: город пользователя 
- os: операционная система телефона пользователя 
- source: источник трафика (органический или рекламный)
