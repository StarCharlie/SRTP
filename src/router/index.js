import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  {
    path: "/",
    name: "mainHome",
    component: () => import("../MainView/HomeView.vue"),
  },
  {
    path: "/Infor",
    name: "information",
    component: () => import("../MainView/InforView.vue"),
  },
  {
    path: "/login",
    name: "login",
    component: () => import("../UserView/LoginView.vue"),
  },
  {
    path: "/register",
    name: "register",
    component: () => import("../UserView/RegisterView.vue"),
  },
  {
    path: "/search",
    name: "search",
    component: () => import("../MainView/SearchView.vue"),
  },
  // 用户端
  {
    path: "/user",
    name: "user",
    component: () => import("../UserView/UserMainView.vue"),
    children: [
      {
        path: "",
        name: "showinfo",
        component: () => import("../UserView/ShowInfo.vue"),
      },
      {
        path: "infoeditor",
        name: "infoeditor",
        component: () => import("../UserView/InfoEditor.vue"),
      },
      {
        path: "accounteditor",
        name: "accounteditor",
        component: () => import("../UserView/AccountEditor.vue"),
      },
      {
        path: "myarticle",
        name: "myarticle",
        component: () => import("../UserView/MyArticle.vue"),
      },
    ],
  },
// 知识图谱端
  {
    path: "/graph",
    name: "graph",
    component: () => import("../GraphView/GraphMainView.vue"),
    children: [
      {
        path: "",
        name: "showAllGraph",
        component: () => import("../GraphView/ShowAllGraph.vue"),
      },
      {
        path: "QA",
        name: "QA",
        component: () => import("../GraphView/QAView.vue"),
      },
      {
        path: "config",
        name: "config",
        component: () => import("../GraphView/ConfigView.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;