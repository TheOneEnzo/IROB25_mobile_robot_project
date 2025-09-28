// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from irob_interfaces:srv/GetGoal.idl
// generated code does not contain a copyright notice

#ifndef IROB_INTERFACES__SRV__DETAIL__GET_GOAL__BUILDER_HPP_
#define IROB_INTERFACES__SRV__DETAIL__GET_GOAL__BUILDER_HPP_

#include "irob_interfaces/srv/detail/get_goal__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace irob_interfaces
{

namespace srv
{


}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::irob_interfaces::srv::GetGoal_Request>()
{
  return ::irob_interfaces::srv::GetGoal_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace irob_interfaces


namespace irob_interfaces
{

namespace srv
{

namespace builder
{

class Init_GetGoal_Response_goal_y
{
public:
  explicit Init_GetGoal_Response_goal_y(::irob_interfaces::srv::GetGoal_Response & msg)
  : msg_(msg)
  {}
  ::irob_interfaces::srv::GetGoal_Response goal_y(::irob_interfaces::srv::GetGoal_Response::_goal_y_type arg)
  {
    msg_.goal_y = std::move(arg);
    return std::move(msg_);
  }

private:
  ::irob_interfaces::srv::GetGoal_Response msg_;
};

class Init_GetGoal_Response_goal_x
{
public:
  Init_GetGoal_Response_goal_x()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_GetGoal_Response_goal_y goal_x(::irob_interfaces::srv::GetGoal_Response::_goal_x_type arg)
  {
    msg_.goal_x = std::move(arg);
    return Init_GetGoal_Response_goal_y(msg_);
  }

private:
  ::irob_interfaces::srv::GetGoal_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::irob_interfaces::srv::GetGoal_Response>()
{
  return irob_interfaces::srv::builder::Init_GetGoal_Response_goal_x();
}

}  // namespace irob_interfaces

#endif  // IROB_INTERFACES__SRV__DETAIL__GET_GOAL__BUILDER_HPP_
