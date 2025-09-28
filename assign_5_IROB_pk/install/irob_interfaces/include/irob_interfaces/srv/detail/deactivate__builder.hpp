// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from irob_interfaces:srv/Deactivate.idl
// generated code does not contain a copyright notice

#ifndef IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__BUILDER_HPP_
#define IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__BUILDER_HPP_

#include "irob_interfaces/srv/detail/deactivate__struct.hpp"
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
auto build<::irob_interfaces::srv::Deactivate_Request>()
{
  return ::irob_interfaces::srv::Deactivate_Request(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace irob_interfaces


namespace irob_interfaces
{

namespace srv
{

namespace builder
{

class Init_Deactivate_Response_message
{
public:
  explicit Init_Deactivate_Response_message(::irob_interfaces::srv::Deactivate_Response & msg)
  : msg_(msg)
  {}
  ::irob_interfaces::srv::Deactivate_Response message(::irob_interfaces::srv::Deactivate_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::irob_interfaces::srv::Deactivate_Response msg_;
};

class Init_Deactivate_Response_success
{
public:
  Init_Deactivate_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Deactivate_Response_message success(::irob_interfaces::srv::Deactivate_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_Deactivate_Response_message(msg_);
  }

private:
  ::irob_interfaces::srv::Deactivate_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::irob_interfaces::srv::Deactivate_Response>()
{
  return irob_interfaces::srv::builder::Init_Deactivate_Response_success();
}

}  // namespace irob_interfaces

#endif  // IROB_INTERFACES__SRV__DETAIL__DEACTIVATE__BUILDER_HPP_
