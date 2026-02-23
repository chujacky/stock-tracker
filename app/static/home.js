
(() => {
    let url = "get_data";
    const green = '#e6ffe6';
    const red = '#ffe6e6';
    let data;

    if (params = window.location.search) {
        url += params;
    }

    const styleCell = (cell) => {
        if (cell == null) return;

        color = cell == "Under" || cell == "Yes" ? green : red;

        return {
            'style': `background-color: ${color}`,
        };
    }

    fetch(url).then((response) => response.json())
        .then((responseData) => {
            const loaderContainer = document.querySelector(".loader-container")
            const tableContainer = document.querySelector(".table-container")
            const tableWrapper = document.querySelector(".table-wrapper");
            const updateTimeText = document.querySelector(".last-update");

            [data, categories, lastUpdate] = responseData;

            const grid = new gridjs.Grid({
                sort: true,
                search: true,
                pagination: {
                    limit: 25,
                    summary: true
                },
                columns: [
                    {
                        name: "Ticker",
                        formatter: (cell) => new gridjs.html(`<a href="https://seekingalpha.com/symbol/${cell}" target="_blank">${cell}</a>`)
                    },
                    "Category",
                    "Close",
                    {
                        name: 'Change',
                        attributes: (cell) => {
                            // add these attributes to the td elements only
                            if (cell == null) return;

                            color = "none";
                            formatChange = parseFloat(cell);

                            if (formatChange > 0.05) {
                                color = green;
                            }

                            if (formatChange < -0.05) {
                                color = red;
                            }

                            return {
                                'style': `background-color: ${color}; color: ${formatChange > 0 ? 'green' : 'red'}`,
                            };
                        },
                        formatter: (cell) => parseFloat(cell * 100).toFixed(2) + "%"
                    },
                    {
                        name: "52 Low",
                        data: (data) => data.low_52
                    },
                    {
                        name: "52 High",
                        data: (data) => data.high_52
                    },
                    {
                        name: 'RSI',
                        attributes: (cell) => {
                            // add these attributes to the td elements only
                            if (cell == null) return;

                            color = cell > 30 && cell < 70 ? green : red;

                            return {
                                'style': `background-color: ${color}`,
                            };
                        }
                    },
                    {
                        name: 'ma50',
                        attributes: (cell) => {
                            return styleCell(cell)
                        }
                    },
                    {
                        name: 'ma100',
                        attributes: (cell) => {
                            return styleCell(cell)
                        }
                    },
                    {
                        name: 'ma200',
                        attributes: (cell) => {
                            return styleCell(cell)
                        }
                    },
                    {
                        name: 'Vol',
                        data: (row) => row["vol>25%"],
                        attributes: (cell) => {
                            return styleCell(cell)
                        }
                    },],
                data: data,
            }).render(tableWrapper);

            updateTimeText.innerHTML += lastUpdate;
            tableContainer.style.display = "block";
            loaderContainer.style.display = "none";

            const gridContainer = document.querySelector(".gridjs-container");
            const sortHeader = document.createElement("div");
            const dropdown = document.createElement("select");
            let options = "<option value=''>All</option>";

            categories.forEach(element => {
                options += `<option value="${element}">${element}</option>`
            });

            sortHeader.classList.add("select", "is-primary");
            dropdown.innerHTML = options;
            sortHeader.append(dropdown);
            tableWrapper.before(sortHeader);
            dropdown.addEventListener("change", () => {
                const category = dropdown.value;

                grid.updateConfig({
                    data: category ? data.filter(stock => stock.category == category) : data,
                }).forceRender();
            })
        });
})()