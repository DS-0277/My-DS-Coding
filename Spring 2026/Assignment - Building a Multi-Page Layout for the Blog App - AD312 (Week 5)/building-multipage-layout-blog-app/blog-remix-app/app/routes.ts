import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
    index("routes/_index.jsx"),
    route("about", "routes/about.jsx"),
    route("post/:postId", "routes/post.$postId.jsx")
] satisfies RouteConfig;
