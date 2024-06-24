import DataTable from "datatables.net-dt";
import "datatables.net-responsive-dt";
import languageRU from "datatables.net-plugins/i18n/ru.mjs";
import { uploader } from "..";
import DownloadIcon from "bootstrap-icons/icons/download.svg";
import TrashIcon from "bootstrap-icons/icons/trash.svg";
import RestartIcon from "bootstrap-icons/icons/arrow-clockwise.svg";

function getStatusPriority(status) {
    const priorities = {
        PREPARING: -1,
        SUCCESS: 2,
        FAILED: 3,
        ACCEPTED: 4,
        STARTED: 5,
    };
    return priorities[status] || 0;
}

export class KptTable {
    constructor() {
        this.el = null;
        this.table = null;
        this.refreshInterval = null;

        this.baseOptions = {
            language: languageRU,
            responsive: true,
            destroy: true,
            order: [[2, "desc"]],
        };

        this.taskOptions = {
            ajax: {
                url: "/data/tasks",
                dataSrc: "",
            },
            columns: [
                { data: "id", title: "ID", className: "table-id" },
                { data: "name", title: "Участок", className: "table-name" },
                { data: null, title: "Статус", className: "table-stats" },
                { data: "created_at", title: "Дата добавления", className: "table-date" },
                { data: null, title: "Действия", orderable: false, className: "table-actions" },
            ],
            columnDefs: [
                {
                    targets: 2,
                    render: function (data, type, row) {
                        const task_status = row.status || { state: "REJECTED" };

                        const display = `
                            <div class="table-stats__container">
                                <div>${KptTable.getStatus(task_status, "Конвертация выписки:")}</div>
                            </div>
                        `;

                        if (type === "sort") return getStatusPriority(task_status.state);

                        return display;
                    },
                },
                {
                    targets: 3,
                    render: function (data, type, row) {
                        return KptTable.getDate(row.created_at);
                    },
                },
                {
                    targets: 4,
                    render: (data, type, row) => {
                        const display = document.createElement("div");
                        display.className = "kpt-table-actions";
                        display.innerHTML = `
                            <a class="kpt-table-action">${DownloadIcon}</a>
                            <button class="kpt-table-action">${TrashIcon}</button>
                            <button class="kpt-table-action">${RestartIcon}</button>
                        `;

                        const buttons = display.querySelectorAll(".kpt-table-action");
                        buttons[0].onclick = () => uploader.downloadFile("tasks", row.id, row.name, buttons[0]);
                        buttons[1].onclick = () => uploader.deleteTask(row.id, buttons[1]);
                        buttons[2].onclick = () => uploader.restartTask(row.id, buttons[2]);

                        return display;
                    },
                },
            ],

            ...this.baseOptions,
        };
        this.groupOptions = {
            ajax: {
                url: "/data/groups",
                dataSrc: "",
            },
            columns: [
                { data: "id", title: "ID", className: "table-id" },
                { data: "name", title: "Группа", className: "table-name" },
                { data: null, title: "Статистика", className: "table-stats" },
                { data: "created_at", title: "Дата добавления", className: "table-date" },
                { data: null, title: "Действия", orderable: false, className: "table-actions" },
            ],
            columnDefs: [
                {
                    targets: 2,
                    render: function (data, type, row) {
                        const statistics = row.statistics;
                        const display = `
                            <div class="table-stats__container">
                                <div class="kpt-badge info">
                                    <p>Загружено:</p><span>${statistics.loaded}</span>
                                </div>
                                <div class="kpt-badge warning">
                                    <p>В обработке:</p><span>${statistics.in_progress}</span>
                                </div>
                                <div class="kpt-badge success">
                                    <p>Готово:</p><span>${statistics.completed}</span>
                                </div>
                                <div class="kpt-badge danger">
                                    <p>Ошибка:</p><span>${statistics.failed}</span>
                                </div>
                                <div class="kpt-badge primary">
                                    <p>Осталось:</p><span>${statistics.remaining}</span>
                                </div>
                            </div>
                        `;

                        if (type === "sort") return statistics.in_progress;

                        return display;
                    },
                },
                {
                    targets: 3,
                    render: function (data, type, row) {
                        return KptTable.getDate(row.created_at);
                    },
                },
                {
                    targets: 4,
                    render: (data, type, row) => {
                        const display = document.createElement("div");
                        display.className = "kpt-table-actions";
                        display.innerHTML = `
                            <a class="kpt-table-action">${DownloadIcon}</a>
                            <button class="kpt-table-action">${TrashIcon}</button>
                            <button class="kpt-table-action">${RestartIcon}</button>
                        `;

                        const buttons = display.querySelectorAll(".kpt-table-action");
                        buttons[0].onclick = () => uploader.downloadFile("groups", row.id, row.name, buttons[0]);
                        buttons[1].onclick = () => uploader.deleteGroup(row.id, buttons[1]);
                        buttons[2].onclick = () => uploader.restartGroup(row.id, buttons[2]);

                        return display;
                    },
                },
            ],

            ...this.baseOptions,
        };
    }

    init() {
        this.renderTable();
        this.initSwitcher();
        // this.startUpdate();

        return this;
    }

    renderTable() {
        this.el = document.createElement("table");
        this.el.className = "stripe hover row-border";
        document.querySelector(".kpt-table-body").appendChild(this.el);
    }

    initTable(tableType = "tasks") {
        if (tableType === "tasks") this.table = new DataTable(this.el, this.taskOptions);
        else if (tableType === "groups") this.table = new DataTable(this.el, this.groupOptions);
    }

    startUpdate() {
        this.refreshInterval = setInterval(() => {
            this.table.ajax.reload(null, false);
        }, 5000);
    }

    stopUpdate() {
        if (this.refreshInterval) clearInterval(this.refreshInterval);
        this.refreshInterval = null;
    }

    update() {
        this.table.ajax.reload(null, false);
    }

    static getStatus(status, message = "") {
        const state = status.state;
        const error = status.error || "";
        const statuses = {
            ACCEPTED: `<div class="kpt-badge info"><p>${message}</p><span>Принято к исполнению</span></div>`,
            STARTED: `<div class="kpt-badge warning"><p>${message}</p><span>В обработке</span></div>`,
            SUCCESS: `<div class="kpt-badge success"><p>${message}</p><span>Готово</span></div>`,
            FAILED: `<div class="kpt-badge danger"><p>${message}</p><span>Ошибка</span></div><div class="kpt-badge danger"><p>${error}</p></div>`,
            CANCELLED: `<div class="kpt-badge primary"><p>${message}</p><span>Отменено</span>`,
            REJECTED: ``,
        };

        return statuses[state] || statuses["REJECTED"];
    }

    static getDate(date) {
        const d = new Date(date + "Z");
        return d.toLocaleString(undefined, {
            year: "numeric",
            month: "long",
            day: "numeric",
            hour: "numeric",
            minute: "numeric",
        });
    }

    initSwitcher() {
        const switcher = document.querySelector("#table-switcher");
        let tableType = localStorage.getItem("tableType") || "tasks";

        switcher.addEventListener("click", (e) => {
            tableType = e.target.checked ? "groups" : "tasks";
            this.stopUpdate();
            this.initTable(tableType);
            this.startUpdate();
            localStorage.setItem("tableType", tableType);
        });

        switcher.checked = tableType === "groups";
        switcher.dispatchEvent(new Event("click"));
    }
}
