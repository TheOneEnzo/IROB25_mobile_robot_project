// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from irob_interfaces:srv/AtGoal.idl
// generated code does not contain a copyright notice

#ifndef IROB_INTERFACES__SRV__DETAIL__AT_GOAL__BUILDER_HPP_
#define IROB_INTERFACES__SRV__DETAIL__AT_GOAL__BUILDER_HPP_

#include "irob_interfaces/srv/detail/at_goal__struct.hpp"
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
auto build<::irob_interfaces::srv::AtGoal_Request>()
{
  return ::irob_interfaces::srv::AtGoal_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace irob_interfaces


namespace irob_interfaces
{

namespace srv
{

namespace builder
{

class Init_AtGoal_Response_message
{
public:
  explicit Init_AtGoal_Response_message(::irob_interfaces::srv::AtGoal_Response & msg)
  : msg_(msg)
  {}
  ::irob_interfaces::srv::AtGoal_Response message(::irob_interfaces::srv::AtGoal_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::irob_interfaces::srv::AtGoal_Response msg_;
};

class Init_AtGoal_Response_success
{
public:
  Init_AtGoal_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AtGoal_Response_message success(::irob_interfaces::srv::AtGoal_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_AtGoal_Response_message(msg_);
  }

private:
  ::irob_interfaces::srv::AtGoal_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::irob_interfaces::srv::AtGoal_Response>()
{
  return irob_interfaces::srv::builder::Init_AtGoal_Response_success();
}

}  // namespace irob_interfaces

#endif  // IROB_INTERFACES__SRV__DETAIL__AT_GOAL__BUILDER_HPP_
