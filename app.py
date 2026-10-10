import streamlit as st
import pandas as pd
import plotly.express as px

from database import (
    init_db,
    insert_query,
    get_queries,
    is_recent_duplicate,
    update_query_status,
)


st.set_page_config(
    page_title="Student Query Analytics",
    page_icon="🎓",
    layout="wide",
)

init_db()

st.title("🎓 Student Query Analytics System")
st.write("Submit a student query and track its progress.")

submit_tab, records_tab, analytics_tab = st.tabs(
    ["Submit a Query", "View Submitted Queries", "Analytics Dashboard"]
)


with submit_tab:
    st.header("Submit a Student Query")

    with st.form("query_submission_form", clear_on_submit=True):
        student_name = st.text_input(
            "Student Name",
            placeholder="Enter your name",
        )

        title = st.text_input(
            "Query Title",
            placeholder="e.g. Missing CAT marks",
        )

        description = st.text_area(
            "Describe your query",
            placeholder="Explain the issue you need help with...",
        )

        category = st.selectbox(
            "Query Category",
            [
                "Academic",
                "Fees and Finance",
                "Registration",
                "ICT Support",
                "Student Affairs",
                "Other",
            ],
        )

        department = st.selectbox(
            "Responsible Department",
            [
                "Academic Registry",
                "Finance",
                "Computer Science",
                "ICT",
                "Student Affairs",
                "Other",
            ],
        )

        priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"],
            index=1,
        )

        submitted = st.form_submit_button(
            "Submit Query",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not student_name.strip():
            st.error("Please enter your name.")
        elif not title.strip():
            st.error("Please enter a query title.")
        elif not description.strip():
            st.error("Please describe your query.")
        else:
            cleaned_name = student_name.strip()
            cleaned_title = title.strip()
            cleaned_description = description.strip()

            duplicate_id = is_recent_duplicate(
                student_name=cleaned_name,
                title=cleaned_title,
                description=cleaned_description,
                category=category,
                department=department,
                priority=priority,
            )

            if duplicate_id is not None:
                st.warning(
                    "This query appears to have already been submitted. "
                    f"Existing reference: #{duplicate_id}. "
                    "Please check the Submitted Queries tab."
                )
            else:
                query_id = insert_query(
                    student_name=cleaned_name,
                    title=cleaned_title,
                    description=cleaned_description,
                    category=category,
                    department=department,
                    priority=priority,
                )

                st.success(
                    "Your query was submitted successfully! "
                    f"Your reference number is #{query_id}."
                )
                st.info(
                    "Your query is now recorded with Pending status. "
                    "You can check its progress in the Submitted Queries tab."
                )


with records_tab:
    st.header("Submitted Queries")

    if "status_update_message" in st.session_state:
        st.success(st.session_state.pop("status_update_message"))

    queries = get_queries()

    if not queries:
        st.info(
            "No queries have been submitted yet. "
            "Submit your first query using the other tab."
        )
    else:
        df = pd.DataFrame(queries)
        st.metric("Total Queries", len(df))

        st.subheader("Search Queries")
        search_term = st.text_input(
            "Search by student name, title, or description",
            placeholder="e.g. missing CAT marks",
            key="query_search",
        )

        working_df = df.copy()
        if search_term.strip():
            search_text = search_term.strip().lower()
            search_mask = (
                working_df["student_name"].fillna("").str.lower().str.contains(
                    search_text, regex=False
                )
                | working_df["title"].fillna("").str.lower().str.contains(
                    search_text, regex=False
                )
                | working_df["description"].fillna("").str.lower().str.contains(
                    search_text, regex=False
                )
            )
            working_df = working_df[search_mask].copy()

        if working_df.empty:
            st.info("No queries match your search.")
        else:
            st.caption(f"{len(working_df)} matching queries found.")

            st.subheader("Filter Queries")
            filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

            with filter_col1:
                selected_status = st.selectbox(
                    "Filter by Status",
                    ["All"] + sorted(working_df["status"].dropna().unique().tolist()),
                )

            with filter_col2:
                selected_department = st.selectbox(
                    "Filter by Department",
                    ["All"] + sorted(working_df["department"].dropna().unique().tolist()),
                )

            with filter_col3:
                selected_category = st.selectbox(
                    "Filter by Category",
                    ["All"] + sorted(working_df["category"].dropna().unique().tolist()),
                )

            with filter_col4:
                selected_priority = st.selectbox(
                    "Filter by Priority",
                    ["All"] + sorted(working_df["priority"].dropna().unique().tolist()),
                )

            filtered_df = working_df.copy()

            if selected_status != "All":
                filtered_df = filtered_df[filtered_df["status"] == selected_status]

            if selected_department != "All":
                filtered_df = filtered_df[
                    filtered_df["department"] == selected_department
                ]

            if selected_category != "All":
                filtered_df = filtered_df[
                    filtered_df["category"] == selected_category
                ]

            if selected_priority != "All":
                filtered_df = filtered_df[
                    filtered_df["priority"] == selected_priority
                ]

            st.subheader("Filtered Results")
            st.caption(f"{len(filtered_df)} matching queries found.")

            display_columns = [
                "id",
                "title",
                "category",
                "department",
                "priority",
                "status",
                "created_at",
            ]

            if filtered_df.empty:
                st.info("No queries match the selected filters.")
            else:
                st.dataframe(
                    filtered_df[display_columns],
                    use_container_width=True,
                    hide_index=True,
                )

                query_ids = filtered_df["id"].tolist()
                selected_id = st.selectbox(
                    "Select a query to view its details",
                    query_ids,
                    format_func=lambda query_id: (
                        f"#{query_id} - "
                        f"{filtered_df.loc[filtered_df['id'] == query_id, 'title'].iloc[0]}"
                    ),
                )

                selected_query = next(
                    query for query in queries if query["id"] == selected_id
                )

                st.subheader(
                    f"Query #{selected_query['id']}: "
                    f"{selected_query['title']}"
                )
                st.write("**Description:**", selected_query["description"])
                st.write("**Student:**", selected_query["student_name"])
                st.write("**Category:**", selected_query["category"])
                st.write("**Department:**", selected_query["department"])
                st.write("**Status:**", selected_query["status"])

                st.divider()
                st.subheader("Update Query Status")

                status_options = ["Pending", "In Progress", "Resolved"]
                current_status = selected_query.get("status", "Pending")
                status_index = (
                    status_options.index(current_status)
                    if current_status in status_options
                    else 0
                )

                new_status = st.selectbox(
                    "Select the new status",
                    status_options,
                    index=status_index,
                    key=f"status_select_{selected_id}",
                )

                if st.button(
                    "Save Status",
                    type="primary",
                    key=f"save_status_{selected_id}",
                ):
                    if new_status == current_status:
                        st.info("The query already has this status.")
                    else:
                        update_query_status(selected_id, new_status)
                        st.session_state["status_update_message"] = (
                            f"Query #{selected_id} updated to {new_status}."
                        )
                        st.rerun()


with analytics_tab:
    st.header("📊 Student Query Analytics Dashboard")
    st.write("Explore trends and monitor student query resolution.")

    queries = get_queries()

    if not queries:
        st.info(
            "No queries available yet. Submit a query to start "
            "generating analytics."
        )
    else:
        df = pd.DataFrame(queries)
        df["created_at_dt"] = pd.to_datetime(df["created_at"], errors="coerce")
        df["resolved_at_dt"] = pd.to_datetime(df["resolved_at"], errors="coerce")

        total_queries = len(df)
        pending_queries = (df["status"] == "Pending").sum()
        in_progress_queries = (df["status"] == "In Progress").sum()
        resolved_queries = (df["status"] == "Resolved").sum()

        resolution_rate = (
            resolved_queries / total_queries * 100 if total_queries > 0 else 0
        )

        st.subheader("Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Total Queries", total_queries)
        col2.metric("Pending", int(pending_queries))
        col3.metric("In Progress", int(in_progress_queries))
        col4.metric("Resolved", int(resolved_queries))
        st.metric("Resolution Rate", f"{resolution_rate:.1f}%")
        st.divider()

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.subheader("Queries by Status")
            status_counts = (
                df["status"]
                .value_counts()
                .reindex(["Pending", "In Progress", "Resolved"], fill_value=0)
                .rename_axis("Status")
                .reset_index(name="Number of Queries")
            )

            fig_status = px.bar(
                status_counts,
                x="Status",
                y="Number of Queries",
                title="Current Query Status",
                text="Number of Queries",
            )
            st.plotly_chart(fig_status, use_container_width=True)

        with chart_col2:
            st.subheader("Queries by Category")
            category_counts = (
                df["category"]
                .value_counts()
                .rename_axis("Category")
                .reset_index(name="Number of Queries")
            )

            fig_category = px.pie(
                category_counts,
                names="Category",
                values="Number of Queries",
                title="Distribution of Student Issues",
                hole=0.35,
            )
            st.plotly_chart(fig_category, use_container_width=True)

        st.divider()
        st.subheader("Time-Based Analysis")

        time_col1, time_col2 = st.columns(2)

        with time_col1:
            st.subheader("Queries Over Time")
            dated_queries = df.dropna(subset=["created_at_dt"]).copy()

            if not dated_queries.empty:
                min_date = dated_queries["created_at_dt"].min().date()
                max_date = dated_queries["created_at_dt"].max().date()

                date_range = st.date_input(
                    "Select submission date range",
                    value=(min_date, max_date),
                    min_value=min_date,
                    max_value=max_date,
                    key="analytics_date_range",
                )

                if len(date_range) == 2:
                    start_date, end_date = date_range
                    dated_queries = dated_queries[
                        dated_queries["created_at_dt"].dt.date.between(
                            start_date, end_date
                        )
                    ]

                if not dated_queries.empty:
                    dated_queries["Date"] = dated_queries["created_at_dt"].dt.date
                    daily_counts = (
                        dated_queries.groupby("Date")
                        .size()
                        .reset_index(name="Number of Queries")
                    )

                    fig_trends = px.line(
                        daily_counts,
                        x="Date",
                        y="Number of Queries",
                        markers=True,
                        title="Daily Query Submissions",
                    )
                    st.plotly_chart(fig_trends, use_container_width=True)
                else:
                    st.info("No valid submission dates are available.")
            else:
                st.info("No valid submission dates are available.")

        with time_col2:
            st.subheader("Resolution Time")
            resolved_df = df[
                (df["status"] == "Resolved")
                & df["created_at_dt"].notna()
                & df["resolved_at_dt"].notna()
            ].copy()

            if not resolved_df.empty:
                resolved_df["Resolution Hours"] = (
                    resolved_df["resolved_at_dt"] - resolved_df["created_at_dt"]
                ).dt.total_seconds() / 3600

                valid_durations = resolved_df[
                    resolved_df["Resolution Hours"] >= 0
                ]

                if not valid_durations.empty:
                    average_hours = valid_durations["Resolution Hours"].mean()
                    average_days = average_hours / 24

                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric(
                        "Average Resolution Time",
                        f"{average_hours:.1f} hours",
                    )
                    metric_col2.metric(
                        "Average Resolution Time",
                        f"{average_days:.2f} days",
                    )

                    fig_resolution = px.bar(
                        valid_durations,
                        x="id",
                        y="Resolution Hours",
                        hover_data=["title", "department"],
                        labels={
                            "id": "Query Reference",
                            "Resolution Hours": "Hours to Resolve",
                        },
                        title="Resolution Time by Query",
                    )
                    st.plotly_chart(fig_resolution, use_container_width=True)
                else:
                    st.info("No valid resolution durations are available yet.")
            else:
                st.info(
                    "Mark at least one query as Resolved to calculate "
                    "resolution times."
                )

        chart_col3, chart_col4 = st.columns(2)

        with chart_col3:
            st.subheader("Queries by Department")
            department_counts = (
                df["department"]
                .value_counts()
                .rename_axis("Department")
                .reset_index(name="Number of Queries")
            )
            fig_department = px.bar(
                department_counts,
                x="Department",
                y="Number of Queries",
                title="Department Workload",
                text="Number of Queries",
            )
            fig_department.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(fig_department, use_container_width=True)

        with chart_col4:
            st.subheader("Queries by Priority")
            priority_order = ["Low", "Medium", "High"]
            priority_counts = (
                df["priority"]
                .value_counts()
                .reindex(priority_order, fill_value=0)
                .rename_axis("Priority")
                .reset_index(name="Number of Queries")
            )
            fig_priority = px.bar(
                priority_counts,
                x="Priority",
                y="Number of Queries",
                title="Priority Distribution",
                text="Number of Queries",
                category_orders={"Priority": priority_order},
            )
            st.plotly_chart(fig_priority, use_container_width=True)
