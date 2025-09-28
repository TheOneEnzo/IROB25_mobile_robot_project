// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from irob_interfaces:srv/GetGoal.idl
// generated code does not contain a copyright notice

#ifndef IROB_INTERFACES__SRV__DETAIL__GET_GOAL__STRUCT_HPP_
#define IROB_INTERFACES__SRV__DETAIL__GET_GOAL__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__irob_interfaces__srv__GetGoal_Request __attribute__((deprecated))
#else
# define DEPRECATED__irob_interfaces__srv__GetGoal_Request __declspec(deprecated)
#endif

namespace irob_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetGoal_Request_
{
  using Type = GetGoal_Request_<ContainerAllocator>;

  explicit GetGoal_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  explicit GetGoal_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->structure_needs_at_least_one_member = 0;
    }
  }

  // field types and members
  using _structure_needs_at_least_one_member_type =
    uint8_t;
  _structure_needs_at_least_one_member_type structure_needs_at_least_one_member;


  // constant declarations

  // pointer types
  using RawPtr =
    irob_interfaces::srv::GetGoal_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const irob_interfaces::srv::GetGoal_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<irob_interfaces::srv::GetGoal_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<irob_interfaces::srv::GetGoal_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      irob_interfaces::srv::GetGoal_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<irob_interfaces::srv::GetGoal_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      irob_interfaces::srv::GetGoal_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<irob_interfaces::srv::GetGoal_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<irob_interfaces::srv::GetGoal_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<irob_interfaces::srv::GetGoal_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__irob_interfaces__srv__GetGoal_Request
    std::shared_ptr<irob_interfaces::srv::GetGoal_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__irob_interfaces__srv__GetGoal_Request
    std::shared_ptr<irob_interfaces::srv::GetGoal_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetGoal_Request_ & other) const
  {
    if (this->structure_needs_at_least_one_member != other.structure_needs_at_least_one_member) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetGoal_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetGoal_Request_

// alias to use template instance with default allocator
using GetGoal_Request =
  irob_interfaces::srv::GetGoal_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace irob_interfaces


#ifndef _WIN32
# define DEPRECATED__irob_interfaces__srv__GetGoal_Response __attribute__((deprecated))
#else
# define DEPRECATED__irob_interfaces__srv__GetGoal_Response __declspec(deprecated)
#endif

namespace irob_interfaces
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct GetGoal_Response_
{
  using Type = GetGoal_Response_<ContainerAllocator>;

  explicit GetGoal_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->goal_x = 0.0;
      this->goal_y = 0.0;
    }
  }

  explicit GetGoal_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->goal_x = 0.0;
      this->goal_y = 0.0;
    }
  }

  // field types and members
  using _goal_x_type =
    double;
  _goal_x_type goal_x;
  using _goal_y_type =
    double;
  _goal_y_type goal_y;

  // setters for named parameter idiom
  Type & set__goal_x(
    const double & _arg)
  {
    this->goal_x = _arg;
    return *this;
  }
  Type & set__goal_y(
    const double & _arg)
  {
    this->goal_y = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    irob_interfaces::srv::GetGoal_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const irob_interfaces::srv::GetGoal_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<irob_interfaces::srv::GetGoal_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<irob_interfaces::srv::GetGoal_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      irob_interfaces::srv::GetGoal_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<irob_interfaces::srv::GetGoal_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      irob_interfaces::srv::GetGoal_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<irob_interfaces::srv::GetGoal_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<irob_interfaces::srv::GetGoal_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<irob_interfaces::srv::GetGoal_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__irob_interfaces__srv__GetGoal_Response
    std::shared_ptr<irob_interfaces::srv::GetGoal_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__irob_interfaces__srv__GetGoal_Response
    std::shared_ptr<irob_interfaces::srv::GetGoal_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const GetGoal_Response_ & other) const
  {
    if (this->goal_x != other.goal_x) {
      return false;
    }
    if (this->goal_y != other.goal_y) {
      return false;
    }
    return true;
  }
  bool operator!=(const GetGoal_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct GetGoal_Response_

// alias to use template instance with default allocator
using GetGoal_Response =
  irob_interfaces::srv::GetGoal_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace irob_interfaces

namespace irob_interfaces
{

namespace srv
{

struct GetGoal
{
  using Request = irob_interfaces::srv::GetGoal_Request;
  using Response = irob_interfaces::srv::GetGoal_Response;
};

}  // namespace srv

}  // namespace irob_interfaces

#endif  // IROB_INTERFACES__SRV__DETAIL__GET_GOAL__STRUCT_HPP_
