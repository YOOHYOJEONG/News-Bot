function createArticleRow(news, index) {
    const article = document.createElement("article")
    article.className = "news-row"

    const rank = document.createElement("span")
    rank.className = "news-rank"
    rank.innerText = String(index + 1).padStart(2, "0")

    const content = document.createElement("div")
    content.className = "news-content"

    const headline = document.createElement("h3")
    headline.className = "news-headline"
    headline.innerText = news.title

    const link = document.createElement("a")
    link.className = "news-link"
    link.href = news.link
    link.innerText = "기사 원문 보기"
    link.target = "_blank"
    link.rel = "noopener noreferrer"

    content.appendChild(headline)
    content.appendChild(link)

    article.appendChild(rank)
    article.appendChild(content)

    return article
}

function formatHeadlineMeta(date) {
    const dateText = new Intl.DateTimeFormat("ko-KR", {
        year: "numeric",
        month: "long",
        day: "numeric",
        weekday: "long",
    }).format(date)

    const timeText = new Intl.DateTimeFormat("ko-KR", {
        hour: "numeric",
        minute: "2-digit",
    }).format(date)

    return `${dateText} · ${timeText}`
}

function updateHeadlineMeta(date = new Date()) {
    const meta = document.getElementById("headlineMeta")
    meta.innerText = formatHeadlineMeta(date)
}

async function loadNews() {
    const container = document.getElementById("news")
    const button = document.getElementById("refreshButton")

    container.innerHTML = '<div class="state-card">뉴스를 불러오는 중입니다.</div>'
    button.disabled = true

    try {
        const res = await fetch("/api/news")
        if (!res.ok) {
            throw new Error(`HTTP ${res.status}`)
        }

        const data = await res.json()
        container.innerHTML = ""
        updateHeadlineMeta(new Date())

        for (const category in data) {
            const articles = data[category]
            const section = document.createElement("section")
            section.className = "news-section"

            const header = document.createElement("div")
            header.className = "section-header"

            const title = document.createElement("h2")
            title.className = "section-title"
            title.innerText = category

            const count = document.createElement("span")
            count.className = "section-count"
            count.innerText = `${articles.length} articles`

            header.appendChild(title)
            header.appendChild(count)
            section.appendChild(header)

            if (!articles || articles.length === 0) {
                const empty = document.createElement("div")
                empty.className = "state-card"
                empty.innerText = "현재 가져올 수 있는 뉴스가 없습니다."
                section.appendChild(empty)
            } else {
                const list = document.createElement("div")
                list.className = "news-list"

                articles.forEach((news, index) => {
                    list.appendChild(createArticleRow(news, index))
                })

                section.appendChild(list)
            }

            container.appendChild(section)
        }
    } catch (error) {
        container.innerHTML = ""

        const message = document.createElement("div")
        message.className = "state-card state-card-error"
        message.innerText = "뉴스를 불러오지 못했습니다. 잠시 후 다시 시도해주세요."
        container.appendChild(message)
        console.error(error)
    } finally {
        button.disabled = false
    }
}

document.getElementById("refreshButton").addEventListener("click", loadNews)
window.addEventListener("DOMContentLoaded", () => {
    updateHeadlineMeta()
    loadNews()
})
